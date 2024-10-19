from starlette.exceptions import HTTPException


class ValidationError(HTTPException):
    pass
