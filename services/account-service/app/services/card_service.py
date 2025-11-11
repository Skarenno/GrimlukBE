import os
from app.models.response_models import CardResponse
from app.data_access.cards import get_cards_by_user_id
from app.models.mappers import map_card_db_to_response

ACCOUNT_LIMIT = os.getenv("ACCOUNT_LIMIT")

 
def get_cards_service(userid: int) -> list[CardResponse]:
    cards = get_cards_by_user_id(userid)
    return [map_card_db_to_response(card) for card in cards]