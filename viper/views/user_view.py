from viper.models.user_model import UserModel
from viper.utils.tools import jsonify, abort
from viper.utils.log_util import logger
from viper.utils import jwt_util
from viper.schemas import v
from viper.schemas.user_schema import access_token_schema


async def get_access_token(request):
    body = await request.json()

    if not v.validate(body, access_token_schema):
        logger.warning(f'validate from get_access_token:\n{v.errors}')
        return abort(400)

    phone_number = body['phone_number']
    password = body['password']

    user_info = await UserModel().get_user_by_phone(phone_number)
    if not user_info:
        return abort(403)

    db_password = user_info['password_hash']
    is_pwd = jwt_util.validate_password(password, db_password)
    if not is_pwd:
        return abort(403)

    access_token = jwt_util.generate_token({'id': user_info['id']})
    jwt_token = {'access_token': access_token, 'token_type': 'bearer'}
    return jsonify(jwt_token)
