from functools import wraps

from viper.utils.tools import abort
from viper.utils import jwt_util
from viper.utils.schemas import User, validate_data
from viper.models.user_model import UserModel


def auth_required(func):
    @wraps(func)
    async def decorated_function(request, *args, **kwargs):
        user_id, _ = jwt_util.verify_token(request)
        db_user = await UserModel().get_user_by_id(user_id)
        if not db_user:
            return abort(401)
        request.state.user = User(**db_user)
        return await func(request, *args, **kwargs)

    return decorated_function


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
