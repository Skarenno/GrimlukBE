from fastapi import APIRouter, Depends, HTTPException

from app.core.authentication import get_jwt_from_request
from app.core.exceptions.service_exceptions import MicroserviceError, MicroserviceUnavailableError
from app.clients.transaction_client import create_transaction
from app.models.requests.transaction_requests import (
    TransactionCreateRequest,
)
from app.models.responses.transaction_responses import (
    SuccessResponse
)


router = APIRouter(prefix="/transaction", tags=["Account"])

@router.post("/create", response_model=SuccessResponse, status_code=201)
async def bff_create_transaction(
    req: TransactionCreateRequest,
    token: str = Depends(get_jwt_from_request)
):
    try:
        return await create_transaction(req, token)
    except MicroserviceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(503, "Account service unavailable")
