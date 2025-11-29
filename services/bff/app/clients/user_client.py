from app.core.http_client import http_request
from app.core.config import settings
from app.models.responses.user_responses import (
    LoginResponse, UserPublicInfo, RefreshTokenResponse, SuccessResponse
)
from app.models.requests.user_requests import UserInfoRequest

async def user_login(username: str, password: str) -> LoginResponse:
    url = f"{settings.USER_SERVICE_URL}/user/login"
    payload = {"username": username, "password": password}

    data = await http_request("POST", url, json=payload, token=None)
    return LoginResponse.model_validate(data)


async def user_register(credentials, info) -> LoginResponse:
    url = f"{settings.USER_SERVICE_URL}/user/register"

    payload = {
        "userCredentials": credentials.model_dump(mode="json"),
        "userInfo": info.model_dump(mode="json")
    }

    data = await http_request("POST", url, json=payload)
    return LoginResponse.model_validate(data)


async def get_user_info(user_id: int, token: str) -> UserPublicInfo:
    url = f"{settings.USER_SERVICE_URL}/user/getUserInfo/{user_id}"

    data = await http_request("GET", url, token=token)
    return UserPublicInfo.model_validate(data)


async def refresh_token(token: str) -> RefreshTokenResponse:
    url = f"{settings.USER_SERVICE_URL}/user/refreshToken"

    data = await http_request("GET", url, token=token)
    return RefreshTokenResponse.model_validate(data)

async def update_user_info(userInfoRequest: UserInfoRequest, token:str):
    url = f"{settings.USER_SERVICE_URL}/user/updateUserInfo"
    data = await http_request("POST", url, json=userInfoRequest.model_dump(), token=token)
    return SuccessResponse.model_validate(data)