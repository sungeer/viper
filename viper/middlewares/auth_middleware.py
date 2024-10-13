from starlette.middleware.base import BaseHTTPMiddleware

from viper.utils import jwt_util
from viper.models.user_model import UserModel


class AuthenticationMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        user_id, _ = await jwt_util.verify_token(request)
        db_user = await UserModel().get_user_by_id(user_id)
        if db_user:
            request.state.user = db_user
        response = await call_next(request)
        return response
