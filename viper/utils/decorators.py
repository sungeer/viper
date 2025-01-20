from functools import wraps

from viper.utils.resp_util import abort
from viper.utils import jwt_util
from viper.utils.schemas import validate_data
from viper.models.user_model import UserModel
from viper.utils.pools import run_in_thread_pool_db


def validate_request(schema):
    def decorator(func):
        @wraps(func)
        async def decorated_function(request, *args, **kwargs):
            data = await request.json()
            validate_data(data, schema)
            return await func(request, *args, **kwargs)

        return decorated_function

    return decorator


def permission_required(permission_name):
    def decorator(func):
        @wraps(func)
        async def decorated_function(request, *args, **kwargs):
            perm = request.state.has_perm
            if perm not in (permission_name,):
                return abort(403)
            return await func(request, *args, **kwargs)

        return decorated_function

    return decorator


def admin_required(func):  # @admin_required
    return permission_required('admin')(func)


def sync_to_async_db(cls):
    def async_run_in_thread_pool(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await run_in_thread_pool_db(func, *args, **kwargs)

        return wrapper

    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value) and not attr_name.startswith('__'):
            setattr(cls, attr_name, async_run_in_thread_pool(attr_value))
    return cls
