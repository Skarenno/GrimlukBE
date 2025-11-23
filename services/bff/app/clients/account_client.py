from app.core.http_client import http_request
from app.core.config import settings

from app.models.requests.account_requests import (
    AccountCreateRequest,
    DeleteAccountRequest,
)
from app.models.responses.account_responses import (
    AccountResponse,
    AccountTypeResponse,
    BranchCodeResponse,
)


async def create_account(req: AccountCreateRequest, token: dict) -> AccountResponse:
    data = await http_request(
        "POST",
        f"{settings.ACCOUNT_SERVICE_URL}/account/create",
        token=token,
        json=req.model_dump(),
    )
    return AccountResponse.model_validate(data)


async def get_accounts(user_id: int, token: dict):
    data = await http_request(
        "GET",
        f"{settings.ACCOUNT_SERVICE_URL}/account/getAccounts/{user_id}",
        token=token,
    )
    return [AccountResponse.model_validate(a) for a in data]


async def get_account_types(token:dict):
    data = await http_request(
        "GET",
        f"{settings.ACCOUNT_SERVICE_URL}/account/getAccountTypes",
        token=token
    )
    return [AccountTypeResponse.model_validate(t) for t in data]


async def get_branch_codes(token:dict):
    data = await http_request(
        "GET",
        f"{settings.ACCOUNT_SERVICE_URL}/account/getBranchCodes",
        token=token
    )
    return [BranchCodeResponse.model_validate(b) for b in data]


async def delete_account(req: DeleteAccountRequest, token: dict):
    data = await http_request(
        "POST",
        f"{settings.ACCOUNT_SERVICE_URL}/account/delete",
        token=token,
        json=req.model_dump(),
    )
    return AccountResponse.model_validate(data)
