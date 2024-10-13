from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException


def create_app():
    app = FastAPI()

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


def register_errors(app):
    from viper.utils.log_util import logger
    from viper.utils.tools import abort

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc):
        # message = exc.detail
        return abort(exc.status_code)

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc):
        logger.exception(exc)
        return abort(500)


def register_routers(app):
    from viper.routers import chat_view
    from viper.routers import user_view
    app.include_router(chat_view.route)
    app.include_router(user_view.route)


app = create_app()
