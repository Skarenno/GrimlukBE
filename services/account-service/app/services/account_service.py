import os
from app.models.request_models import AccountCreateRequest
from app.models.response_models import AccountResponse
from app.models.mappers import map_account_create_to_db, map_account_db_to_response, map_account_type_db_to_response
from app.data_access.account import insert_account, get_accounts_by_userid
from app.data_access.account_types import get_all_account_types
from app.exceptions.service_exception import AccountLimitError, UserDoesNotExistError
from app.external.user_service import check_user_valid

ACCOUNT_LIMIT = os.getenv("ACCOUNT_LIMIT")

 
def check_create_valid(bearer_token:str, user_id:int):
    if not check_user_valid(user_id, bearer_token):
        print(user_id)
        raise UserDoesNotExistError

    accounts = get_accounts_by_userid(user_id)
    
    if len(accounts) >= int(ACCOUNT_LIMIT):
        raise AccountLimitError
    



def create_account_service(request:AccountCreateRequest, bearer_token:str) -> AccountResponse:
    check_create_valid(bearer_token, request.user_id)
    new_account = map_account_create_to_db(request)
    return map_account_db_to_response(insert_account(new_account))

def get_accounts_service(userid: int, bearer_token:str) -> list[AccountResponse]:
    if not check_user_valid(userid, bearer_token):
        raise UserDoesNotExistError
    
    accounts = get_accounts_by_userid(userid)
    return [map_account_db_to_response(account) for account in accounts]

def get_account_types():
    account_types = get_all_account_types()
    return [map_account_type_db_to_response(account_type) for account_type in account_types]