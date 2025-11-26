from fastapi import APIRouter, Depends, HTTPException

from app.core.authentication import get_jwt_from_request
from app.core.exceptions.service_exceptions import MicroserviceError, MicroserviceUnavailableError
from app.clients.account_client import (
    create_account,
    get_accounts,
    get_account_types,
    get_branch_codes,
    delete_account
)
from app.clients.user_client import get_user_info
from app.models.requests.account_requests import (
    AccountCreateRequest,
    DeleteAccountRequest,
)
from app.models.responses.account_responses import (
    AccountResponse,
    AccountTypeResponse,
    BranchCodeResponse,
)


router = APIRouter(prefix="/account", tags=["Account"])

@router.post("/create", response_model=AccountResponse, status_code=201)
async def bff_create_account(
    req: AccountCreateRequest,
    token: str = Depends(get_jwt_from_request)
):
    try:
        return await create_account(req, token)
    except MicroserviceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(503, "Account service unavailable")

@router.get("/getAccounts/{user_id}", response_model=list[AccountResponse])
async def bff_get_accounts(
    user_id: int,
    token: str = Depends(get_jwt_from_request)
):
    try:
        await get_user_info(user_id=user_id, token=token)
        return await get_accounts(user_id, token)
    except MicroserviceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(503, "Account service unavailable")


@router.get("/getAccountTypes", response_model=list[AccountTypeResponse])
async def bff_get_account_types( token: str = Depends(get_jwt_from_request)):
    try:
        return await get_account_types(token=token)
    except MicroserviceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(503, "Account service unavailable")

@router.get("/getBranchCodes", response_model=list[BranchCodeResponse])
async def bff_get_branch_codes(token: str = Depends(get_jwt_from_request)):
    try:
        return await get_branch_codes(token=token)
    except MicroserviceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(503, "Account service unavailable")

@router.post("/delete", response_model=AccountResponse)
async def bff_delete_account(
    req: DeleteAccountRequest,
    token: str = Depends(get_jwt_from_request)
):
    try:
        await get_user_info(req.userId, token)
        return await delete_account(req, token)
    except MicroserviceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(503, "Account service unavailable")
