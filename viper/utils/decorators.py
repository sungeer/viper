from functools import wraps

from viper.utils.tools import abort
from viper.utils import jwt_util
from viper.models.user_model import UserModel
from viper.utils.schemas import User


def auth_required(func):
    @wraps(func)
    async def decorated(request, *args, **kwargs):
        user_id, _ = await jwt_util.verify_token(request)
        db_user = await UserModel().get_user_by_id(user_id)
        if not db_user:
            return abort(401)
        request.state.user = User(**db_user)
        return await func(request, *args, **kwargs)

    return decorated
