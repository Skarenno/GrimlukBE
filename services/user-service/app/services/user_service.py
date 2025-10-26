from sqlalchemy.orm import Session
from app.models.mappers import map_user_info_to_db, map_user_db_to_response
from app.models.request_models import *
from app.models.db_models import *
from app.data_access.user_credentials import add_user_credentials, get_user_credentials_by_username
from app.data_access.access_log import add_access_log
from app.data_access.user_info import get_user_info_by_user_id, get_user_info_by_username, upsert_user_info
from app.utils.authentication import hash_password, verify_password, generate_jwt
from app.exceptions.service_exceptions import *
from datetime import datetime

def register_user_service(request:UserLoginRequest):
    existing = get_user_credentials_by_username(request.username)
    if existing:
        raise UserAlreadyExistsError

    new_user = UserCredentialsModel(
        username=request.username,
        password=hash_password(request.password)
    )

    new_user = add_user_credentials(new_user)
    return generate_jwt(new_user.username)


def login_user_service(request:UserLoginRequest, ip_address:str):
    db_user_credentials = get_user_credentials_by_username(request.username)
    
    if(not db_user_credentials):
            raise UserDoesNotExistError
    if(not verify_password(request.password, db_user_credentials.password)):
            insert_access_log(request, ip_address, successful=False)
            raise PasswordInvalidError

    db_user_info = get_user_info_by_username(request.username)
    insert_access_log(request,ip_address)
    return (generate_jwt(db_user_credentials.username), map_user_db_to_response(db_user_info))

def get_user_info_service(user_id:str):
    db_user = get_user_info_by_user_id(user_id)
    if not db_user or not db_user.id:
         raise UserDoesNotExistError
    
    return map_user_db_to_response(db_user)
     

def upsert_user_info_service(request:UserInfoRequest):
    db_user = get_user_info_by_username(request.username)
    db_user = map_user_info_to_db(request, existing_user=db_user)

    return map_user_db_to_response(upsert_user_info(db_user))

    
def insert_access_log(request:UserLoginRequest, ip_address:str, successful=True):
    log_insert = UserAccessLogModel(
        username = request.username,
        ip_address = ip_address,
        successful = successful,
        access_timestamp = datetime.now()
    )

    add_access_log(log_insert)
    return