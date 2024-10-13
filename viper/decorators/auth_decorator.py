from functools import wraps

from viper.utils.tools import abort


def requires_auth(func):
    @wraps(func)
    async def decorated_function(request, *args, **kwargs):
        if not getattr(request.state, 'user', None):
            return abort(401)
        return await func(request, *args, **kwargs)

    return decorated_function
