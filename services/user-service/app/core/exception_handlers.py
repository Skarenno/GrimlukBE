import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    UserDoesNotExistError,
    UserAlreadyExistsError,
    JwtPermissionError,
    PasswordInvalidError
)

logger = logging.getLogger("user-service-errors")

def register_exception_handlers(app):

    @app.exception_handler(UserDoesNotExistError)
    async def user_not_found(_, exc):
        logger.exception(exc)
        return JSONResponse(
            status_code=404,
            content={"error": "User does not exist"}
        )

    @app.exception_handler(UserAlreadyExistsError)
    async def existing_user(_, exc):
        logger.exception(exc)
        return JSONResponse(
            status_code=409,
            content={"error": "User already exists"}
        )

    @app.exception_handler(PasswordInvalidError)
    async def invalid_password(_, exc):
        logger.exception(exc)
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid username or password"}
        )

    @app.exception_handler(JwtPermissionError)
    async def permission_error(_, exc):
        logger.exception(exc)
        return JSONResponse(
            status_code=403,
            content={"error": "Not allowed to access this user"}
        )

    @app.exception_handler(Exception)
    async def unhandled(_, exc):
        logger.exception(exc)
        return JSONResponse(
            status_code=500,
            content={"error": "Unexpected internal error"}
        )
