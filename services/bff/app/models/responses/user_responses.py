from pydantic import BaseModel
from typing import Optional

class UserPublicInfo(BaseModel):
    id: int
    username: str
    tax_code:str
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    residence_address_1: Optional[str] = None
    residence_address_2: Optional[str] = None
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