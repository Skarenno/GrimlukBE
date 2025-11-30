import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions.authentication_exception import *
from app.core.exceptions.service_exception import *

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
            content={"error": "Authorization error - cannot permit this operation"},
        )


    @app.exception_handler(TransactionError)
    async def transaction_handler(request: Request, exc: JwtPermissionError):
        logger.exception(
            "TransactionError at %s %s",
            request.method,
            request.url.path,
            exc_info=exc,
        )
        return JSONResponse(
            status_code=401,
            content={"error": "TransactionError error - cannot create transaction"},
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
