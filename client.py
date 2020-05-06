import asyncio
import aiohttp
from loguru import logger


class AppMetric:
    def __init__(self, host, port=8050):
        self.push_base_url = f'http://{host}:{port}/metric/{{}}'

    def send_value(self, metric_uuid, value, tag=None, timestamp=None):
        asyncio.ensure_future(self._send(metric_uuid, value))

    def send_event(self, metric_uuid, tag=None, timestamp=None):
        asyncio.ensure_future(self._send(metric_uuid, 1))

    async def _send(self, metric_uuid, value, tag=None, timestamp=None):
        payload = {
            'value': value
        }
        if tag:
            payload['tag'] = tag
        if timestamp:
            payload['timestamp'] = timestamp

        async with aiohttp.ClientSession() as session:
            async with session.post(self.push_base_url.format(metric_uuid), json=payload) as r:
                if r.status != 200:
                    data = await r.json()
                    logger.warning(f'[LOGGER] Error send value {r.status}:{data}')
                else:
                    logger.debug(f'[LOGGER] Sent value {data}')
