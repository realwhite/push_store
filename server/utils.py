import uuid
import json
import datetime
from functools import wraps

import yaml
from cerberus import Validator
from aiohttp import web

def load_conf(path: str) -> dict:
    with open(path) as file:
        conf = yaml.safe_load(file)
    return conf

def get_uuid() -> str:
    return str(uuid.uuid4()).replace('-', '')

def validate(schema):
    # @wraps
    def wrapper(fn):
        async def deco(_self, request):
            if request.method == 'GET':
                data = request.query
            else:
                data = await request.json()

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
