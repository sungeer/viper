from datetime import datetime, timedelta

import bcrypt  # python -m pip install bcrypt
import jwt  # python -m pip install pyjwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from starlette.authentication import AuthenticationError

from viper.core import settings
from viper.utils.errors import TokenExpiredError


def set_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


def validate_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def generate_token(data: dict):
    token_data = data.copy()  # data = {'id': 3}
    expiration_delta = timedelta(minutes=settings.CONF('EXPIRE_MINUTES', cast=int))
    expiration_time = datetime.now() + expiration_delta
    token_data.update({'exp': expiration_time.timestamp()})
    encoded_token = jwt.encode(token_data, settings.CONF('SECRET_KEY'), algorithm=settings.CONF('ALGORITHM'))
    return encoded_token


def verify_token(token: str):
    secret_key = settings.CONF('SECRET_KEY')
    jwt_algorithm = settings.CONF('ALGORITHM')

    try:
        payload = jwt.decode(token, secret_key, algorithms=[jwt_algorithm])
        user_id = payload.get('id')
        if not user_id:
            raise AuthenticationError('Invalid JWT: missing field id')
    except ExpiredSignatureError:
        raise TokenExpiredError('Token has expired')
    except InvalidTokenError as exc:
        raise AuthenticationError(f'Invalid token: {str(exc)}')
    return user_id
