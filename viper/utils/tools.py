import json
from datetime import datetime, date
from decimal import Decimal

from starlette.responses import JSONResponse


class JsonExtendEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (tuple, list, datetime)):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')
        return super().default(obj)


class JsonExtendResponse(JSONResponse):

    def render(self, content):
        return json.dumps(content, cls=JsonExtendEncoder).encode('utf-8')


def jsonify(content):
    return JsonExtendResponse(content)


def dict_to_json(data):
    if not data:
        data = {}
    return json.dumps(data, cls=JsonExtendEncoder)


def dict_to_json_ea(data=None):
    return json.dumps(data, cls=JsonExtendEncoder, ensure_ascii=False, indent=4)


def json_to_dict(json_data):
    return json.loads(json_data)
