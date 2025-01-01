from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from viper.utils import http_client, redis_util
from viper.utils.db_util import db
from viper.utils.log_util import logger
from viper.utils.tools import jsonify_exc
from viper.utils.errors import ValidationError
from viper.urls import chat_url, user_url


def create_app():
    app = Starlette()

    register_errors(app)
    register_events(app)
    register_middlewares(app)
    register_routers(app)
    return app


def register_events(app):
    @app.on_event('startup')
    async def startup():
        await db.connect()

    @app.on_event('shutdown')
    async def shutdown():
        await db.disconnect()
        await http_client.close_httpx()
        await redis_util.close_redis()


def register_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://127.0.0.1'],  # ['*'] 允许所有来源
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def register_errors(app):
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request, exc):
        logger.opt(exception=True).warning(exc)
        return jsonify_exc(422, exc.detail)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        logger.opt(exception=True).warning(exc)
        return jsonify_exc(exc.status_code, exc.detail)

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.exception(exc)
        return jsonify_exc(500)


def register_routers(app):
    app.mount('/chat', chat_url.chat_url)
    app.mount('/user', user_url.user_url)


app = create_app()
