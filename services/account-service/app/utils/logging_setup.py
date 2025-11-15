import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.authentication_exception import *
from app.exceptions.service_exception import *

logger = logging.getLogger("api-errors")


def register_exception_handlers(app):

    @app.exception_handler(JwtPermissionError)
    async def jwt_permission_handler(request: Request, exc: JwtPermissionError):
        logger.exception(
            "JwtPermissionError at %s %s",
            request.method,
            request.url.path,
            exc_info=exc,
        )
        return JSONResponse(
            status_code=401,
            content={"error": "Authorization error: cannot create for other users"},
        )

    @app.exception_handler(UserDoesNotExistError)
    async def user_not_exist_handler(request: Request, exc: UserDoesNotExistError):
        logger.exception(
            "UserDoesNotExistError at %s %s",
            request.method,
            request.url.path,
            exc_info=exc,
        )
        return JSONResponse(
            status_code=401,
            content={"error": "Authorization error: user does not exist"},
        )

    @app.exception_handler(UserServiceError)
    async def user_service_handler(request: Request, exc: UserServiceError):
        logger.exception(
            "UserServiceError at %s %s",
            request.method,
            request.url.path,
            exc_info=exc,
        )
        return JSONResponse(
            status_code=500,
            content={"error": "Service error: cannot retrieve user information"},
        )

    @app.exception_handler(AccountLimitError)
    async def account_limit_handler(request: Request, exc: AccountLimitError):
        logger.exception(
            "AccountLimitError at %s %s",
            request.method,
            request.url.path,
            exc_info=exc,
        )
        return JSONResponse(
            status_code=200,
            content={"error": "Account error: account limit reached for user"},
        )

    @app.exception_handler(Exception)
    async def generic_handler(request: Request, exc: Exception):
        logger.exception(
            "Generic error at %s %s",
            request.method,
            request.url.path,
            exc_info=exc,
        )
        return JSONResponse(
            status_code=500,
            content={"error": "Generic server error"},
        )
