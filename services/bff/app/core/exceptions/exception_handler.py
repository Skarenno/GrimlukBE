import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions.authentication_exceptions import *
from app.core.exceptions.service_exceptions import *

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

    @app.exception_handler(MicroserviceUnavailableError)
    async def ms_unavailable_handler(request: Request, exc: MicroserviceUnavailableError):
        return JSONResponse(
            status_code=503,
            content={"error": "A microservice is unavailable. Please try again later."}
        )


    @app.exception_handler(MicroserviceError)
    async def ms_error_handler(request: Request, exc: MicroserviceError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )
    
    
    @app.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, exc: Exception):
        print("UNEXPECTED BFF ERROR:", exc)
        return JSONResponse(
            status_code=500,
            content={"error": "Unexpected BFF error"}
        )