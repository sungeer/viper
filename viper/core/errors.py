from starlette.requests import Request
from starlette.exceptions import HTTPException

from viper.utils.log_util import logger
from viper.utils.resp_util import jsonify_exc
from viper.utils.errors import ValidationError


async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.opt(exception=True).warning(exc)
    return jsonify_exc(422, exc.args)


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.opt(exception=True).warning(exc)
    return jsonify_exc(exc.status_code, exc.detail)


async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(exc)
    return jsonify_exc(500)


register_errors = {
    ValidationError: validation_exception_handler,
    HTTPException: http_exception_handler,
    Exception: global_exception_handler,
}
