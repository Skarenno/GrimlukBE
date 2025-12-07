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


    @app.exception_handler(AccountLimitError)
    async def account_limit_handler(request: Request, exc: AccountLimitError):
        logger.exception(
            "AccountLimitError at %s %s",
            request.method,
            request.url.path,
            exc_info=exc,
        )
        return JSONResponse(
            status_code=400,
            content={"error": "Account error - account limit reached for user"},
        )

    @app.exception_handler(CardRetrievalError)
    async def card_retrieval_handler(request: Request, exc: AccountLimitError):
        logger.exception(
            "CardRetrievalError at %s %s",
            request.method,
            request.url.path,
            exc_info=exc,
        )
        return JSONResponse(
            status_code=400,
            content={"error": "Card error - could not retrieve cards information"},
        )
    
    @app.exception_handler(AccountRetrievalError)
    async def card_retrieval_handler(request: Request, exc: AccountLimitError):
        logger.exception(
            "AccountRetrievalError at %s %s",
            request.method,
            request.url.path,
            exc_info=exc,
        )
        return JSONResponse(
            status_code=400,
            content={"error": "Account error - could not retrieve accunt information"},
        )
    
    @app.exception_handler(AccountBlockingFundError)
    async def card_retrieval_handler(request: Request, exc: AccountLimitError):
        logger.exception(
            "AccountBlockingFundError at %s %s",
            request.method,
            request.url.path,
            exc_info=exc,
        )
        return JSONResponse(
            status_code=400,
            content={"error": "Account blocking error - could not transfer this amount"},
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
