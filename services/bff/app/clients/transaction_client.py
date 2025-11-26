from app.core.http_client import http_request
from app.core.config import settings
from app.models.requests.transaction_requests import (
    TransactionCreateRequest,
)
from app.models.responses.transaction_responses import (
    SuccessResponse,
    TransactionResponse
)


async def create_transaction(req: TransactionCreateRequest, token: dict) -> SuccessResponse:
    data = await http_request(
        "POST",
        f"{settings.TRANSACTION_SERVICE_URL}/transaction/create",
        token=token,
        json=req.model_dump(mode="json"),
    )
    return SuccessResponse.model_validate(data)

async def get_by_user_id(user_id:int, token:dict) -> list[TransactionResponse]:
    data = await http_request(
        "GET",
        f"{settings.TRANSACTION_SERVICE_URL}/transaction/getByUserId/{user_id}",
        token=token
    )

    return [TransactionResponse.model_validate(transaction) for transaction in data]