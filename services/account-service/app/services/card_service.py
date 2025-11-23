import os
from datetime import datetime
from app.models.response_models import CardResponse
from app.data_access.cards import get_cards_by_user_id, insert_card, get_card_by_id, update_card
from app.services.account_service import get_account_by_id
from app.core.exceptions.service_exception import AccountRetrievalError, CardRetrievalError
from app.models.request_models import CardCreateRequest, CardUpdateRequest
from app.models.mappers import map_card_db_to_response, map_card_create_to_db
from app.utils.enums import AccountStatus
from app.core.authentication import check_jwt_user_auth

ACCOUNT_LIMIT = os.getenv("ACCOUNT_LIMIT")

 
def get_cards_service(userid: int, jwt_payload:dict) -> list[CardResponse]:
    check_jwt_user_auth(user_id=userid, jwt_payload=jwt_payload)
    cards = get_cards_by_user_id(userid)
    return [map_card_db_to_response(card) for card in cards]


def create_card_service(createRequest:CardCreateRequest, jwt_payload:dict):
    check_jwt_user_auth(user_id=createRequest.user_id, jwt_payload=jwt_payload)
    check_request(createRequest)
    db_card = insert_card(map_card_create_to_db(createRequest))
    return map_card_db_to_response(db_card)

def update_card_service(card_id:int, updateRequest:CardUpdateRequest, jwt_payload:dict):
    db_card = get_card_by_id(card_id)
    if db_card is None:
        raise CardRetrievalError
    check_jwt_user_auth(user_id=db_card.user_id, jwt_payload=jwt_payload)

    field_updates = updateRequest.model_dump(exclude_unset=True, exclude_none=True, exclude_defaults=True)

    for field, value in field_updates.items():
        setattr(db_card, field, value)

    updated = update_card(db_card)
    if not updated:
        raise CardRetrievalError
    
    return map_card_db_to_response(updated)

def check_request(createRequest:CardCreateRequest):
    account = get_account_by_id(createRequest.account_id)

    if not account or account.status == AccountStatus.DELETED.value:
        raise AccountRetrievalError

    if account.user_id != createRequest.user_id:
        raise AccountRetrievalError