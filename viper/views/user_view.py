from viper.models.user_model import UserModel
from viper.utils.tools import jsonify, abort
from viper.utils import jwt_util
from viper.utils.validation_util import validate_data
from viper.schemas.user_schema import access_token_schema


async def get_access_token(request):
    body = await request.json()

    validate_data(body, access_token_schema)

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
