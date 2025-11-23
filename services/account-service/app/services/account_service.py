import os
from app.models.request_models import AccountCreateRequest, DeleteAccountRequest
from app.models.response_models import AccountResponse
from app.models.mappers import map_account_create_to_db, map_account_db_to_response, map_account_type_db_to_response, map_branch_codes_db_to_response
from app.data_access.cards import get_cards_by_account_id, update_card
from app.data_access.account import insert_account, get_accounts_by_userid, get_account_by_id, update_account, get_active_accounts_by_userid
from app.data_access.account_types import get_all_account_types
from app.data_access.branch_codes import get_all_branch_codes
from app.core.exceptions.service_exception import AccountLimitError, AccountRetrievalError, CardRetrievalError
from app.utils.enums import CardStatus, AccountStatus
from app.core.authentication import check_jwt_user_auth

ACCOUNT_LIMIT = os.getenv("ACCOUNT_LIMIT")

def get_account_types_service():
    account_types = get_all_account_types()
    return [map_account_type_db_to_response(account_type) for account_type in account_types]

def get_branch_codes_service():
    branch_codes = get_all_branch_codes()
    return [map_branch_codes_db_to_response(branch_code) for branch_code in branch_codes]


def check_create_valid(user_id:int):
    active_accounts = get_active_accounts_by_userid(user_id)
    
    if len(active_accounts) >= int(ACCOUNT_LIMIT):
        raise AccountLimitError


def create_account_service(request:AccountCreateRequest, jwt_user:dict) -> AccountResponse:
    check_jwt_user_auth(jwt_payload=jwt_user, user_id=request.user_id)
    check_create_valid(request.user_id)
    new_account = map_account_create_to_db(request)
    return map_account_db_to_response(insert_account(new_account))


def get_accounts_service(userid: int, jwt_user:dict) -> list[AccountResponse]:
    check_jwt_user_auth(jwt_payload=jwt_user, user_id=userid)
    accounts = get_accounts_by_userid(userid)
    accounts.sort(key= lambda account:account.status)
    return [map_account_db_to_response(account) for account in accounts]



def delete_account_service(request:DeleteAccountRequest, jwt_user:dict):
    delete_accont = get_account_by_id(request.deleteId)
    if not delete_accont or delete_accont.status == AccountStatus.DELETED.value:
        raise AccountRetrievalError
    
    check_jwt_user_auth(jwt_payload=jwt_user, user_id=delete_accont.user_id)

    transfer_account = get_account_by_id(request.transferId)



    #transfer funds LOGIC
    try:
        cards = get_cards_by_account_id(delete_accont.id)
        for card in cards:
            card.status = CardStatus.BLOCKED.value
            card = update_card(card)
    except:
        raise CardRetrievalError
    
    delete_accont.status = AccountStatus.DELETED.value
    return map_account_db_to_response(update_account(delete_accont))
