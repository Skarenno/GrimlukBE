from app.core.http_client import http_request
from app.core.config import settings

from app.models.requests.card_requests import (
    CardCreateRequest,
    CardUpdateRequest
)

from app.models.responses.card_responses import CardResponse


async def create_card(req: CardCreateRequest, token: str) -> CardResponse:
    data = await http_request(
        "POST",
        f"{settings.ACCOUNT_SERVICE_URL}/card/create",
        token=token,
        json=req.model_dump(),
    )
    return CardResponse.model_validate(data)


async def get_cards_by_user(user_id: int, token: str):
    data = await http_request(
        "GET",
        f"{settings.ACCOUNT_SERVICE_URL}/card/getByUser/{user_id}",
        token=token,
    )
    return [CardResponse.model_validate(c) for c in data]


async def update_card(req: CardUpdateRequest, token: str):
    data = await http_request(
        "POST",
        f"{settings.ACCOUNT_SERVICE_URL}/card/update",
        token=token,
        json=req.model_dump(),
    )
    return CardResponse.model_validate(data)
