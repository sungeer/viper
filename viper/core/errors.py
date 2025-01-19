from starlette.exceptions import HTTPException

from viper.utils.log_util import logger
from viper.utils.resp_util import jsonify_exc
from viper.utils.errors import ValidationError

register_errors = {
    ValidationError: lambda request, exc: (
        logger.opt(exception=True).warning(exc) or jsonify_exc(422, exc.args)
    ),
    HTTPException: lambda request, exc: (
        logger.opt(exception=True).warning(exc) or jsonify_exc(exc.status_code, exc.detail)
    ),
    Exception: lambda request, exc: (
        logger.exception(exc) or jsonify_exc(500)
    ),
}
