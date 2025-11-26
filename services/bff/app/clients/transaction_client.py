from app.core.http_client import http_request
from app.core.config import settings
from app.models.requests.transaction_requests import (
    TransactionCreateRequest,
)
from app.models.responses.transaction_responses import (
    SuccessResponse
)


async def create_transaction(req: TransactionCreateRequest, token: dict) -> SuccessResponse:
    data = await http_request(
        "POST",
        f"{settings.TRANSACTION_SERVICE_URL}/account/create",
        token=token,
        json=req.model_dump_json(),
    )
    return SuccessResponse.model_validate(data)