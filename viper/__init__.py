from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException


def create_app():
    app = Starlette()

    register_errors(app)
    register_events(app)
    register_middlewares(app)
    register_routers(app)
    return app


def register_events(app):
    from viper.utils.db_util import db

    @app.on_event('startup')
    async def startup():
        await db.connect()

    @app.on_event('shutdown')
    async def shutdown():
        await db.disconnect()

        from viper.utils import http_client
        await http_client.close_httpx()

        from viper.utils import redis_util
        await redis_util.close_redis()


def register_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['127.0.0.1'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    from viper.middlewares import auth_middleware

    app.add_middleware(auth_middleware.AuthenticationMiddleware)


def register_errors(app):
    from viper.utils.log_util import logger
    from viper.utils.tools import abort

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        logger.opt(exception=True).warning(exc)
        return abort(exc.status_code)

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.exception(exc)
        return abort(500)


def register_routers(app):
    from viper.urls import chat_url, user_url
    app.router.mount('/chat', chat_url.chat_url)
    app.router.mount('/user', user_url.user_url)


app = create_app()
