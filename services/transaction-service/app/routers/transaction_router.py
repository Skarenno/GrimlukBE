from fastapi import APIRouter, Request, Depends
from fastapi import status
from app.models.request_models import (
    TransactionAccountGetRequest,
    TransactionCreateRequest
)
from app.models.response_models import (
    SuccessResponse,
    TransactionResponse
)
from app.services.transaction_service import create_transaction_service, get_transactions_by_user_id_service, get_transactions_by_account_list_service

router = APIRouter(prefix="/transaction")

@router.post(
    "/create",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED
)
def create_transaction(req: TransactionCreateRequest, request: Request):
    jwt_user = request.state.user
    return create_transaction_service(req, jwt_user)
    

@router.get(
    "/getByUserId/{user_id}",
    response_model=list[TransactionResponse],
    status_code=status.HTTP_200_OK
)
def get_transactions_by_user_id(user_id:int, request:Request):
    jwt_user = request.state.user
    return get_transactions_by_user_id_service(user_id, jwt_user)

@router.post(
    "/getByAccountList",
    response_model=list[TransactionResponse],
    status_code=status.HTTP_200_OK
)
def get_transactions_by_account_list(transactionRequest: TransactionAccountGetRequest, request:Request):
    jwt_user = request.state.user
    return get_transactions_by_account_list_service(transactionRequest, jwt_user)