from fastapi import APIRouter, Depends, HTTPException
from app.clients.user_client import (
    user_login,
    user_register,
    get_user_info,
    refresh_token,
    update_user_info
)
from app.models.requests.user_requests import (
    UserLoginRequest,
    UserRegisterRequest,
    UserInfoRequest
)
from app.models.responses.user_responses import (
    LoginResponse,
    UserPublicInfo,
    RefreshTokenResponse,
    SuccessResponse
)
from app.core.exceptions.service_exceptions import MicroserviceError, MicroserviceUnavailableError
from app.core.authentication import get_jwt_from_request

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/login", response_model=LoginResponse)
async def login(req: UserLoginRequest):
    try:
        return await user_login(req.username, req.password)
    except MicroserviceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(status_code=503, detail="User service unavailable")

@router.post("/register", response_model=LoginResponse)
async def register(req: UserRegisterRequest):
    try:
        return await user_register(req.userCredentials, req.userInfo)
    except MicroserviceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(status_code=503, detail="User service unavailable")

@router.get("/info/{user_id}", response_model=UserPublicInfo)
async def get_info(user_id: int, token: dict = Depends(get_jwt_from_request)):
    try:
        return await get_user_info(user_id, token)
    except MicroserviceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(status_code=503, detail="User service unavailable")

@router.get("/refresh", response_model=RefreshTokenResponse)
async def refresh(token: dict = Depends(get_jwt_from_request)):
    try:
        return await refresh_token(token)
    except MicroserviceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(status_code=503, detail="User service unavailable")

@router.post("/update", response_model=SuccessResponse)
async def update(req: UserInfoRequest, token: dict = Depends(get_jwt_from_request)):
    try:
        await update_user_info(req, token)
        return SuccessResponse(message="User info updated successfully")
    except MicroserviceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except MicroserviceUnavailableError:
        raise HTTPException(status_code=503, detail="User service unavailable")
