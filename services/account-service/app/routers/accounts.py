from fastapi import APIRouter, Request 
from fastapi.responses import JSONResponse
from fastapi import status
from app.models.request_models import *
from app.models.response_models import *
from app.services.account_service import create_account_service, get_accounts_service, get_account_types
from app.utils.authentication import check_jwt_user_auth
from app.exceptions.authentication_exception import *
from app.exceptions.service_exception import *


router = APIRouter(prefix="/account")


@router.post("/create", response_model=AccountResponse)
def create_account(account_create_request:AccountCreateRequest, request:Request):
    try:
        bearer_token = request.headers.get("Authorization")
        user = request.state.user

        check_jwt_user_auth(user, account_create_request.username)
        account = create_account_service(account_create_request, bearer_token)
    except JwtPermissionError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error" : "Authorization error: cannot create for other users"}
        )
    except UserDoesNotExistError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error" : "Authorization error: user does not exist"}
        ) 
    except UserServiceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error" : "Service error: cannot retrieve user information"}
        ) 
    except AccountLimitError:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"error" : "Account error: account limit reached for user"}
        ) 
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error" : "Generic server error"}
        ) 
    
    return account

@router.get("/getAccounts/{user_id}", response_model=list[AccountResponse])
def get_user_accounts(user_id: int, request:Request):
    try:
        bearer_token = request.headers.get("Authorization")
        accounts = get_accounts_service(user_id, bearer_token)
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error" : "Generic server error"}
        ) 
    
    return accounts
    
@router.get("/getAccountTypes", response_model=list[AccountTypeResponse])
def get_types(request:Request):
    try:
        account_types = get_account_types()
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error" : "Generic server error"}
        ) 

    return account_types


