from fastapi import APIRouter, Request 
from fastapi import status
from app.models.request_models import CardCreateRequest, CardUpdateRequest
from app.models.response_models import CardResponse
from app.services.card_service import get_cards_service, create_card_service, update_card_service

router = APIRouter(prefix="/card")


@router.get("/getByUser/{user_id}", response_model=list[CardResponse])
def get_user_cards_list(user_id: int, request:Request):
    return get_cards_service(user_id)

@router.post("/create", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_card(createCardRequest:CardCreateRequest, request:Request):
    bearer_token = request.headers.get("Authorization")
    return create_card_service(createCardRequest, bearer_token)

@router.patch("/update/{card_id}")
def update_card(card_id: int, updateCardRequest:CardUpdateRequest, request:Request):
    bearer_token = request.headers.get("Authorization")
    return update_card_service(card_id, updateCardRequest, bearer_token)


