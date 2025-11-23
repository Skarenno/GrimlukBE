from datetime import datetime
from app.models.mappers import (
    map_user_info_to_db,
    map_user_db_to_response
)
from app.models.request_models import (
    UserLoginRequest,
    UserInfoRequest,
    UserRegisterRequest
)
from app.models.db_models import (
    UserCredentialsModel,
    UserAccessLogModel
)
from app.data_access.user_credentials import (
    add_user_credentials,
    get_user_credentials_by_username
)
from app.data_access.access_log import add_access_log
from app.data_access.user_info import (
    get_user_info_by_user_id,
    get_user_info_by_username,
    upsert_user_info
)
from app.core.authentication import (
    hash_password,
    verify_password,
    generate_jwt
)
from app.core.exceptions import (
    UserAlreadyExistsError,
    UserDoesNotExistError,
    PasswordInvalidError,
    JwtPermissionError
)


def register_user_service(req: UserRegisterRequest):

    existing = get_user_credentials_by_username(req.userCredentials.username)
    if existing:
        raise UserAlreadyExistsError(
            f"User {req.userCredentials.username} already exists"
        )

    new_user = UserCredentialsModel(
        username=req.userCredentials.username,
        password=hash_password(req.userCredentials.password)
    )
    add_user_credentials(new_user)

    user_info = upsert_user_info(
        map_user_info_to_db(req.userInfo, existing_user=None)
    )

    access_token, refresh_token = generate_jwt(new_user.username, user_info.id)

    return access_token, refresh_token, map_user_db_to_response(user_info)



def login_user_service(req: UserLoginRequest, ip_address: str):

    db_user_credentials = get_user_credentials_by_username(req.username)
    if not db_user_credentials:
        insert_access_log(req, ip_address, successful=False)
        raise UserDoesNotExistError(f"User {req.username} not found")

    if not verify_password(req.password, db_user_credentials.password):
        insert_access_log(req, ip_address, successful=False)
        raise PasswordInvalidError("Invalid password")

    db_user_info = get_user_info_by_username(req.username)
    insert_access_log(req, ip_address, successful=True)

    access_token, refresh_token = generate_jwt(db_user_credentials.username, db_user_info.id)

    return access_token, refresh_token, map_user_db_to_response(db_user_info)



def get_user_info_service(user_id: int):

    db_user = get_user_info_by_user_id(user_id)
    if not db_user or not db_user.id:
        raise UserDoesNotExistError(f"User ID {user_id} not found")
    return map_user_db_to_response(db_user)



def refresh_jwt_token(jwt_payload: dict):
    username = jwt_payload.get("sub")
    user_id = jwt_payload.get("id")
    return generate_jwt(username, user_id)



def upsert_user_info_service(req: UserInfoRequest, jwt_payload: dict):
    if req.username != jwt_payload["sub"]:
        raise JwtPermissionError("Cannot modify another user's profile")

    existing = get_user_info_by_username(req.username)
    db_user = map_user_info_to_db(req, existing_user=existing)

    saved_user = upsert_user_info(db_user)
    return map_user_db_to_response(saved_user)



def insert_access_log(req: UserLoginRequest, ip_address: str, successful=True):
    log_entry = UserAccessLogModel(
        username=req.username,
        ip_address=ip_address,
        successful=successful,
        access_timestamp=datetime.now()
    )

    add_access_log(log_entry)
