from datetime import datetime

from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def succ(data=None, message='成功'):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                'code': 200,
                'message': message,
                'data': data,
                'success': True,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        )
    )
