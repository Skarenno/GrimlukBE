from fastapi import APIRouter, Request, Depends
from fastapi import status
from app.models.request_models import (
    TransactionCreateRequest
)
from app.models.response_models import (
    SuccessResponse
)
from app.services.transaction_service import create_transaction_service

router = APIRouter(prefix="/transaction")

@router.post(
    "/create",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED
)
def create_transaction(req: TransactionCreateRequest, request: Request):
    jwt_user = request.state.user
    return create_transaction_service(req, jwt_user)
    



