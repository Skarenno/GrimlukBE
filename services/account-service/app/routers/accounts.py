from fastapi import APIRouter, Request, Depends
from fastapi import status

from app.models.request_models import (
    AccountCreateRequest,
    DeleteAccountRequest,
)
from app.models.response_models import (
    AccountResponse,
    AccountTypeResponse,
    BranchCodeResponse,
)

from app.services.account_service import (
    create_account_service,
    get_accounts_service,
    get_account_types_service,
    get_branch_codes_service,
    delete_account_service,
)

from app.core.authentication import check_jwt_user_auth


router = APIRouter(prefix="/account")

@router.post(
    "/create",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED
)
def create_account(req: AccountCreateRequest, request: Request):
    jwt_user = request.state.user
    account = create_account_service(req, jwt_user)
    return account


@router.get(
    "/getAccounts/{user_id}",
    response_model=list[AccountResponse]
)
def get_user_accounts(user_id: int, request: Request):
    jwt_user = request.state.user
    accounts = get_accounts_service(user_id, jwt_user=jwt_user)
    return accounts

@router.get(
    "/getAccountTypes",
    response_model=list[AccountTypeResponse]
)
def get_account_types():
    return get_account_types_service()

@router.get(
    "/getBranchCodes",
    response_model=list[BranchCodeResponse]
)
def get_branch_codes():
    return get_branch_codes_service()

@router.post(
    "/delete",
    response_model=AccountResponse
)
def delete_account(req: DeleteAccountRequest, request: Request):
    jwt_user = request.state.user
    deleted = delete_account_service(req, jwt_user=jwt_user)
    return deleted
