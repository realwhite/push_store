import json
import datetime

import yaml
from cerberus import Validator
from aiohttp import web


def load_conf(path: str) -> dict:
    with open(path) as file:
        conf = yaml.safe_load(file)
    return conf


def validate(schema):
    def wrapper(fn):
        async def deco(_self, request):
            if request.method == 'GET':
                data = request.query
            else:
                try:
                    data = await request.json()
                except json.decoder.JSONDecodeError:
                    data = {}

            v = Validator(schema)
            is_valid = v.validate(data)

            if is_valid:
                result = await fn(_self, request, v.document)
                return result
            else:
                return web.json_response({'success': False, 'errors': v.errors}, status=422)
        return deco
    return wrapper


def json_defaults(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()


def custom_json_dumps(*args, **kwargs):
    kwargs['default'] = json_defaults
    return json.dumps(*args, **kwargs)
