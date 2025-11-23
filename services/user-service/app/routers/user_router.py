from fastapi import APIRouter, Depends, Request
from app.models.request_models import (
    UserLoginRequest, 
    UserRegisterRequest, 
    UserInfoRequest
)
from app.models.response_models import LoginResponse, UserInfoResponse
from app.services.user_service import (
    login_user_service,
    refresh_jwt_token,
    register_user_service,
    upsert_user_info_service,
    get_user_info_service,
)
from app.core.authentication import get_current_user

router = APIRouter(prefix="/user")

@router.post("/login", response_model=LoginResponse)
async def login(req: UserLoginRequest, request: Request):
    ip = request.client.host
    jwt_token, refresh_token, user = login_user_service(req, ip)

    return LoginResponse(
        jwt_token=jwt_token,
        refresh_token=refresh_token,
        user=user
    )

@router.post("/register", response_model=LoginResponse)
async def register(req: UserRegisterRequest):
    jwt_token, refresh_token, user = register_user_service(req)

    return LoginResponse(
        jwt_token=jwt_token,
        refresh_token=refresh_token,
        user=user
    )

@router.get("/refreshToken")
async def refresh(current_user=Depends(get_current_user)):
    jwt_token, refresh_token = refresh_jwt_token(current_user)
    return {"jwt_token": jwt_token, "refresh_token": refresh_token}

@router.post("/updateUserInfo")
async def update_info(req: UserInfoRequest, current_user=Depends(get_current_user)):
    upsert_user_info_service(req, current_user)
    return {"detail": f"{req.username} updated correctly"}

@router.get("/getUserInfo/{user_id}", response_model=UserInfoResponse)
async def get_info(user_id: int, current_user=Depends(get_current_user)):
    user = get_user_info_service(user_id)
    return user
