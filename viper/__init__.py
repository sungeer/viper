from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Mount
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from touch.exts import db, https, redis, logs
from touch.exts.logs import logger, stop_logger


def create_app():
    app = Starlette()

    register_errors(app)
    register_events(app)
    register_middlewares(app)
    register_routers(app)
    return app


def register_errors(app):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        try:
            logger.exception(exc)
        except (Exception,):
            pass
        return JSONResponse(
            {'detail': exc.detail},
            status_code=exc.status_code
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        try:
            logger.exception(exc)
        except (Exception,):
            pass
        return JSONResponse(
            {'detail': 'Internal server error'},
            status_code=500
        )


def register_events(app):
    from touch.exts.db import db

    @app.on_event('startup')
    async def startup():
        await db.connect()

    @app.on_event('shutdown')
    async def shutdown():
        await https.close_httpx()
        await db.disconnect()
        try:
            logs.stop_logger()
        except (Exception,):
            pass
        try:
            await redis.redis_client.aclose()
        except (Exception,):
            pass


def register_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        max_age=600,
    )


def register_routers(app):
    from touch.urls import workflow
    app.router.mount('/workflows', workflow.workflow_url)


app = create_app()
