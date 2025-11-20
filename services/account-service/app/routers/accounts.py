from fastapi import APIRouter, Request 
from fastapi.responses import JSONResponse
from fastapi import status
from app.models.request_models import *
from app.models.response_models import *
from app.services.account_service import create_account_service, get_accounts_service, get_account_types_service, delete_account_service
from app.utils.authentication import check_jwt_user_auth
from app.exceptions.authentication_exception import *
from app.exceptions.service_exception import *

router = APIRouter(prefix="/account")


@router.post("/create", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(account_create_request:AccountCreateRequest, request:Request):
    bearer_token = request.headers.get("Authorization")
    user = request.state.user

    check_jwt_user_auth(user, account_create_request.username)
    account = create_account_service(account_create_request, bearer_token)

    
    return account

@router.get("/getAccounts/{user_id}", response_model=list[AccountResponse])
def get_user_accounts(user_id: int, request:Request):
    bearer_token = request.headers.get("Authorization")
    accounts = get_accounts_service(user_id, bearer_token)

    return accounts
    
@router.get("/getAccountTypes", response_model=list[AccountTypeResponse])
def get_types(request:Request):
    account_types = get_account_types_service()
    return account_types

@router.post("/delete")
def delete_account(delet_account_request:DeleteAccountRequest, request:Request):
    bearer_token = request.headers.get("Authorization")
    delete_account_service(delet_account_request, bearer_token)
    return JSONResponse(status_code=status.HTTP_200_OK)
