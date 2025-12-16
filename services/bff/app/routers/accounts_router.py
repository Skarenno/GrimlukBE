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

@router.post("/create", response_model=AccountResponse, status_code=201,
             summary="Create a new account",
             description="Creates a new bank account for the specified user with the provided details. Requires authentication.",
             responses={
                 201: {"description": "Account created successfully", "model": AccountResponse},
                 400: {"description": "Invalid request data"},
                 401: {"description": "Unauthorized"},
                 503: {"description": "Account service unavailable"}
             })
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

@router.get("/getAccounts/{user_id}", response_model=list[AccountResponse],
            summary="Get user accounts",
            description="Retrieves all accounts associated with the specified user ID. Requires authentication and user verification.",
            responses={
                200: {"description": "Accounts retrieved successfully", "model": list[AccountResponse]},
                401: {"description": "Unauthorized"},
                404: {"description": "User not found"},
                503: {"description": "Account service unavailable"}
            })
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


@router.get("/getAccountTypes", response_model=list[AccountTypeResponse],
            summary="Get available account types",
            description="Retrieves a list of all available account types in the system. Requires authentication.",
            responses={
                200: {"description": "Account types retrieved successfully", "model": list[AccountTypeResponse]},
                401: {"description": "Unauthorized"},
                503: {"description": "Account service unavailable"}
            })
async def bff_get_account_types( token: str = Depends(get_jwt_from_request)):
    try:
        return await get_account_types(token=token)
    except MicroserviceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(503, "Account service unavailable")

@router.get("/getBranchCodes", response_model=list[BranchCodeResponse],
            summary="Get available branch codes",
            description="Retrieves a list of all available branch codes for account creation. Requires authentication.",
            responses={
                200: {"description": "Branch codes retrieved successfully", "model": list[BranchCodeResponse]},
                401: {"description": "Unauthorized"},
                503: {"description": "Account service unavailable"}
            })
async def bff_get_branch_codes(token: str = Depends(get_jwt_from_request)):
    try:
        return await get_branch_codes(token=token)
    except MicroserviceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(503, "Account service unavailable")

@router.post("/delete", response_model=AccountResponse,
             summary="Delete an account",
             description="Deletes the specified account. Optionally transfers remaining balance to another account. Requires authentication and user verification.",
             responses={
                 200: {"description": "Account deleted successfully", "model": AccountResponse},
                 400: {"description": "Invalid request data"},
                 401: {"description": "Unauthorized"},
                 404: {"description": "Account or user not found"},
                 503: {"description": "Account service unavailable"}
             })
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
