import sys
import asyncio

from aiohttp import web
import asyncpg
from asyncpg.exceptions import UniqueViolationError, CannotConnectNowError
from loguru import logger

from server.utils import validate, custom_json_dumps
from server.schemas import CREATE_METRIC, PUSH_METRIC
from server.constants import MetricDataType, MetricStatus


class AppHandlers:
    def __init__(self, app: web.Application):
        self.app = app

    @staticmethod
    def success_response(data: dict, status=200) -> web.Response:
        return web.json_response(
            {'success': True, 'data': data},
            status=status, dumps=custom_json_dumps
        )

    @staticmethod
    def error_response(error: dict, status=422) -> web.Response:
        return web.json_response(
            {'success': False, 'error': error},
            status=status, dumps=custom_json_dumps
        )

    @property
    def db_pool(self):
        return self.app['pool']

    @validate(CREATE_METRIC)
    async def create_metric(self, request: web.Request, data: dict) -> web.Response:
        async with self.db_pool.acquire() as conn:
            async with conn.transaction():
                metric_tbl_name = f"metric_{data['uuid']}"

                try:
                    await conn.execute(
                        'INSERT INTO metrics(uuid, title, datatype, description) VALUES($1, $2, $3, $4);',
                        data['uuid'], data['title'], data['type'], data['description']
                    )
                except UniqueViolationError:
                    return self.error_response('uuid_must_be_unique', status=422)

                metric_datatype = MetricDataType.get_db_type(data['type'])

                await conn.execute(f'''
                    CREATE TABLE {metric_tbl_name} (
                        time TIMESTAMP NOT NULL DEFAULT now(),
                        value {metric_datatype} NULL,
                        tag TEXT NOT NULL DEFAULT ''
                    );
                    SELECT create_hypertable('{metric_tbl_name}', 'time');
                ''')

                logger.info(f"[METRIC] Metric '{data['title']}' added.")

        return self.success_response({'metric_id': data['uuid']})

    async def list_metrics(self, request: web.Request) -> web.Response:
        async with self.db_pool.acquire() as conn:
            async with conn.transaction():
                metrics = await conn.fetch('SELECT * FROM metrics')
                response = [dict(m) for m in metrics]
        return self.success_response({'metrics': response})

    async def update_metric(self, request: web.Request) -> web.Response:
        return self.success_response({})

    async def truncate_metric(self, request: web.Request) -> web.Response:
        metric_uuid = request.match_info['metric_uuid']
        async with self.db_pool.acquire() as conn:
            async with conn.transaction():
                status = await conn.fetchval('SELECT status FROM metrics WHERE uuid = $1', metric_uuid)
                if not status:
                    logger.warning(f'[PUSH] Metric {metric_uuid} not found!')
                    return self.error_response({'metric_uuid': 'not_found'}, status=404)

                if status == MetricStatus.ACTIVE:
                    logger.warning(f'[PUSH] Metric {metric_uuid} is active!')
                    return self.error_response({'status': 'metric must be a paused status'}, status=403)

                await conn.execute(f'TRUNCATE TABLE metric_{metric_uuid}')

        return self.success_response({})

    async def delete_metric(self, request: web.Request) -> web.Response:
        metric_uuid = request.match_info['metric_uuid']
        async with self.db_pool.acquire() as conn:
            async with conn.transaction():
                status = await conn.fetchval('SELECT status FROM metrics WHERE uuid = $1', metric_uuid)

                if not status:
                    logger.warning(f'[PUSH] Metric {metric_uuid} not found!')
                    return self.error_response({'metric_uuid': 'not_found'}, status=404)

                if status == MetricStatus.ACTIVE:
                    logger.warning(f'[PUSH] Metric {metric_uuid} is active!')
                    return self.error_response({'status': 'metric must be a paused status'}, status=403)

                await conn.execute(f'DROP TABLE metric_{metric_uuid}')
                await conn.execute('DELETE FROM metrics WHERE uuid = $1', metric_uuid)

        return self.success_response({})

    @validate(PUSH_METRIC)
    async def push_metric(self, request: web.Request, data: dict) -> web.Response:
        metric_uuid = request.match_info['metric_uuid']
        async with self.db_pool.acquire() as conn:
            async with conn.transaction():
                status = await conn.fetchval('SELECT status FROM metrics WHERE uuid = $1', metric_uuid)

                if not status:
                    logger.warning(f'[PUSH] Metric {metric_uuid} not found!')
                    return self.error_response('not_found', status=404)

                if status != MetricStatus.ACTIVE:
                    logger.warning(f'[PISH] Metric {metric_uuid} is not active!')
                    return self.error_response('invalid_status', status=403)

                fields = ['value']
                if 'time' in data:
                    fields.append('time')
                if 'tag' in data:
                    fields.append('tag')

                fields_str = ', '.join(fields)
                values_str = ', '.join(f'${i}' for i in range(1, len(fields) + 1))

                query_template = f'INSERT INTO metric_{metric_uuid}({fields_str}) VALUES({values_str})'

                await conn.execute(query_template, *[data[f] for f in fields])
                await conn.execute(f'UPDATE metrics SET last_event = now() WHERE uuid = $1', metric_uuid)

                logger.debug(f"[PUSH] Value {data} for metric {metric_uuid} pushed.")

        return self.success_response({'metric_uuid': metric_uuid, 'value': data['value']})

    async def get_metric(self, request: web.Request) -> web.Response:
        async with self.db_pool.acquire() as conn:
            r = await conn.fetchval('select now();')
            logger.info(f'{r}')
        return self.success_response({})


class Application:
    def __init__(self, config: dict):
        self.config = config
        self.webapp = web.Application()
        self.loop = asyncio.get_event_loop()
        self._config_webapp()

        self.loop.run_until_complete(self._config_database())

    def _config_webapp(self):
        _handlers = AppHandlers(self.webapp)
        self.webapp.add_routes([
            web.post('/metrics', _handlers.create_metric),
            web.get('/metrics', _handlers.list_metrics),
            web.put('/metric/{metric_uuid}', _handlers.update_metric),
            web.delete('/metric/{metric_uuid}', _handlers.delete_metric),
            web.post('/metric/{metric_uuid}',  _handlers.push_metric),
            web.post('/metric/{metric_uuid}/truncate',  _handlers.truncate_metric),
            web.get('/metric/{metric_uuid}',  _handlers.get_metric),
        ])

    async def _config_database(self):
        for _ in range(10):
            try:
                self.webapp['pool'] = await asyncpg.create_pool(self.config['database']['dsn'])
                logger.info('[DATABASE] Connection established')
                return
            except (ConnectionRefusedError, CannotConnectNowError) as exc:
                logger.warning(f'[DATABASE] Connection error {exc}')
                await asyncio.sleep(5)

        sys.exit(0)

    def run(self):
        logger.info('[SERVER] Starting application')
        web.run_app(
            self.webapp,
            host=self.config['http']['host'],
            port=self.config['http']['port']
        )
