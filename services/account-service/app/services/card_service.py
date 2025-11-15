import os
from datetime import datetime
from app.models.response_models import CardResponse
from app.data_access.cards import get_cards_by_user_id, insert_card, get_card_by_id, update_card
from app.services.account_service import get_account_by_id
from app.external.user_service import check_user_valid
from app.exceptions.service_exception import AccountRetrievalError, UserDoesNotExistError, CardRetrievalError
from app.models.request_models import CardCreateRequest, CardUpdateRequest
from app.models.mappers import map_card_db_to_response, map_card_create_to_db

ACCOUNT_LIMIT = os.getenv("ACCOUNT_LIMIT")

 
def get_cards_service(userid: int) -> list[CardResponse]:
    cards = get_cards_by_user_id(userid)
    return [map_card_db_to_response(card) for card in cards]


def create_card_service(createRequest:CardCreateRequest, bearer_token:str):
    check_request(createRequest, bearer_token)
    db_card = insert_card(map_card_create_to_db(createRequest))
    return map_card_db_to_response(db_card)

def update_card_service(card_id:int, updateRequest:CardUpdateRequest, bearer_token:str):
    db_card = get_card_by_id(card_id)
    if db_card is None:
        raise CardRetrievalError

    if not check_user_valid(db_card.user_id, bearer_token):
        raise UserDoesNotExistError

    field_updates = updateRequest.model_dump(exclude_unset=True)

    for field, value in field_updates.items():
        setattr(db_card, field, value)
    db_card.updated_at = datetime.now()

    updated = update_card(db_card)
    if not updated:
        raise CardRetrievalError
    
    return map_card_db_to_response(updated)

def check_request(createRequest:CardCreateRequest, bearer_token:str):
    if not check_user_valid(createRequest.user_id, bearer_token):
        raise UserDoesNotExistError

    account = get_account_by_id(createRequest.account_id)

    if not account:
        raise AccountRetrievalError

    if account.user_id != createRequest.user_id:
        raise AccountRetrievalError