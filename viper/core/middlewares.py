from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

origins = [
    'http://127.0.0.1:8000',  # 后端应用使用的端口
    'http://127.0.0.1:8080',  # 前端应用使用的端口
]

register_middlewares = [
    Middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    ),
]
