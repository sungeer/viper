from datetime import datetime, timedelta

import bcrypt  # python -m pip install bcrypt
import jwt  # python -m pip install pyjwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from viper.configs import settings
from viper.utils.log_util import logger


def set_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


def validate_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def generate_token(data: dict):
    token_data = data.copy()  # data = {'id': 3}
    expiration_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expiration_time = datetime.now() + expiration_delta
    token_data.update({'exp': expiration_time.timestamp()})
    encoded_token = jwt.encode(token_data, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_token


def extract_uid(token: str):
    secret_key = settings.jwt_secret_key
    jwt_algorithm = settings.jwt_algorithm
    decoded_payload = jwt.decode(token, secret_key, algorithms=[jwt_algorithm])
    user_id = decoded_payload.get('id')
    return user_id


def verify_token(request):
    authorization_header = request.headers.get('Authorization')
    if authorization_header and authorization_header.startswith('Bearer '):
        jwt_token = authorization_header[len('Bearer '):]
        if not jwt_token:
            logger.warning('Token is empty.')
            return None, 400
    else:
        logger.warning('Authorization header is missing or does not start with Bearer.')
        return None, 400

    try:
        user_id = extract_uid(jwt_token)
    except ExpiredSignatureError:
        logger.opt(exception=True).warning('Token has expired.')
        return None, 401
    except InvalidTokenError:
        logger.opt(exception=True).warning('Token is invalid.')
        return None, 401
    except (Exception,):
        logger.opt(exception=True).error(f'Unexpected error.')
        return None, 500

    if not user_id:
        logger.warning('User ID not found.')
        return None, 404

    return user_id, 200
