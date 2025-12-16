from pydantic import BaseModel, Field
from pydantic import ConfigDict
from typing import Optional
from datetime import datetime

class UserInfoResponse(BaseModel):
    id: int
    username: str
    
    tax_code: str = Field(alias="tax_code")
    email: Optional[str] = Field(None, alias="mail")
    first_name: Optional[str] = Field(None, alias="name")
    last_name: Optional[str] = Field(None, alias="surname")
    phone: Optional[str] = None
    birth_date: Optional[datetime] = None
    gender: Optional[str] = None

    address_line_1: Optional[str] = Field(None, alias="residence_address_1")
    address_line_2: Optional[str] = Field(None, alias="residence_address_2")
    postal_code: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)




class LoginResponse(BaseModel):
    jwt_token: str
    refresh_token: str
    user: UserInfoResponse

    model_config = ConfigDict(from_attributes=True)


class RefreshTokenResponse(BaseModel):
    jwt_token: str
    refresh_token: str

    model_config = ConfigDict(from_attributes=True)

