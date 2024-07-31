from datetime import datetime, timedelta

import bcrypt  # python -m pip install bcrypt
import jwt  # python -m pip install pyjwt
from jwt.exceptions import ExpiredSignatureError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from vrm.configs import settings
from vrm.exts.logger import logger


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


def extract_user_id_from_token(token: str):
    decoded_payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    user_id = decoded_payload.get('id')
    return user_id


def throw_invalid_token_exception():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )


bearer_scheme = HTTPBearer()


# 依赖函数 身份验证
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    user_id = None
    token = credentials.credentials
    try:
        user_id = extract_user_id_from_token(token)
    except ExpiredSignatureError:
        throw_invalid_token_exception()
    except (Exception,):
        throw_invalid_token_exception()
    if not user_id:
        throw_invalid_token_exception()
    return int(user_id)
