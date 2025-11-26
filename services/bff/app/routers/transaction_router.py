from fastapi import APIRouter, Depends, HTTPException

from app.core.authentication import get_jwt_from_request
from app.core.exceptions.service_exceptions import MicroserviceError, MicroserviceUnavailableError
from app.clients.transaction_client import create_transaction, get_by_user_id, get_transactions_by_accounts
from app.models.requests.transaction_requests import (
    TransactionCreateRequest,
    TransactionAccountGetRequest
)
from app.models.responses.transaction_responses import (
    SuccessResponse,
    TransactionResponse
)


router = APIRouter(prefix="/transaction", tags=["Transaction"])

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
        raise HTTPException(503, "Transaction service unavailable")

@router.get("/getByUserId/{user_id}", response_model=list[TransactionResponse], status_code=200)
async def get_transactions_by_user_id(
    user_id: int,
    token: str = Depends(get_jwt_from_request)
):
    try:
        return await get_by_user_id(user_id, token)
    except MicroserviceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(503, "Transaction service unavailable")

@router.post("/getByAccountList", response_model=list[TransactionResponse], status_code=200)
async def get_transactions_by_user_id(
    req: TransactionAccountGetRequest,
    token: str = Depends(get_jwt_from_request)
):
    try:
        return await get_transactions_by_accounts(req, token)
    except MicroserviceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(503, "Transaction service unavailable")
