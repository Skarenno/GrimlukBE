import os
from app.models.response_models import CardResponse
from app.data_access.cards import get_cards_by_user_id, insert_card
from app.services.account_service import get_account_by_id
from app.external.user_service import check_user_valid
from app.exceptions.service_exception import AccountRetrievalError, UserDoesNotExistError
from app.models.request_models import CardCreateRequest
from app.models.mappers import map_card_db_to_response, map_card_create_to_db

ACCOUNT_LIMIT = os.getenv("ACCOUNT_LIMIT")

 
def get_cards_service(userid: int) -> list[CardResponse]:
    cards = get_cards_by_user_id(userid)
    return [map_card_db_to_response(card) for card in cards]


def create_card_service(createRequest:CardCreateRequest, bearer_token:str):
    check_request(createRequest, bearer_token)
    db_card = insert_card(map_card_create_to_db(createRequest))
    return map_card_db_to_response(db_card)


def check_request(createRequest:CardCreateRequest, bearer_token:str):
    if not check_user_valid(createRequest.user_id, bearer_token):
        raise UserDoesNotExistError

    account = get_account_by_id(createRequest.account_id)

    if not account:
        raise AccountRetrievalError

    if account.user_id != createRequest.user_id:
        raise AccountRetrievalError