from fastapi import APIRouter, Depends, HTTPException
from app.core.authentication import get_jwt_from_request
from app.core.exceptions.service_exceptions import MicroserviceError, MicroserviceUnavailableError

from app.clients.card_client import (
    create_card,
    get_cards_by_user,
    update_card,
)

from app.models.requests.card_requests import (
    CardCreateRequest,
    CardUpdateRequest,
)

from app.models.responses.card_responses import CardResponse


router = APIRouter(prefix="/card", tags=["Card"])

@router.post("/create", response_model=CardResponse, status_code=201)
async def bff_create_card(
    req: CardCreateRequest,
    token: dict = Depends(get_jwt_from_request)
):
    try:
        return await create_card(req, token)
    except MicroserviceError as e:
        raise HTTPException(e.status_code, e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(503, "Card service unavailable")

@router.get("/getByUser/{user_id}", response_model=list[CardResponse])
async def bff_get_cards(user_id: int, token: dict = Depends(get_jwt_from_request)):
    try:
        return await get_cards_by_user(user_id, token)
    except MicroserviceError as e:
        raise HTTPException(e.status_code, e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(503, "Card service unavailable")

@router.post("/update", response_model=CardResponse)
async def bff_update_card(
    req: CardUpdateRequest,
    token: dict = Depends(get_jwt_from_request)
):
    try:
        return await update_card(req, token)
    except MicroserviceError as e:
        raise HTTPException(e.status_code, e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(503, "Card service unavailable")
