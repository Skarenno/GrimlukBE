from pydantic import BaseModel
from typing import Optional

class UserPublicInfo(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None


class LoginResponse(BaseModel):
    jwt_token: str
    refresh_token: str
    user: UserPublicInfo


class RefreshTokenResponse(BaseModel):
    jwt_token: str
    refresh_token: str

class SuccessResponse(BaseModel):
    message: str