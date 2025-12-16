from pydantic import BaseModel, Field, field_validator, model_validator, model_serializer
from typing import Optional
from fastapi import HTTPException, status
from app.models.requests.request_validate_utils import validateBody
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class UserInfoRequest(BaseModel) : 
    id: Optional[int] = Field(default=None, example=12345, description="User ID (auto-generated for new users)")
    username: str = Field(..., example="john_doe", description="Unique username")
    tax_code: str = Field(..., example="ABC123456789", description="Tax identification code")
    name: str = Field(..., example="John", description="First name")
    surname: str = Field(..., example="Doe", description="Last name")
    birth_date: str = Field(..., example="1990-01-15T00:00:00", description="Birth date in YYYY-MM-DD format")
    phone: Optional[str] = Field(default=None, example="+1234567890", description="Phone number")
    gender: Optional[str] = Field(default=None, example="M", description="Gender (M/F/O)")
    residence_address_1: Optional[str] = Field(default=None, example="123 Main St", description="Primary residence address")
    residence_address_2: Optional[str] = Field(default=None, example="Apt 4B", description="Secondary residence address")
    city: Optional[str] = Field(default=None, example="NAPOLI", description="City of residence")
    province: Optional[str] = Field(default=None, example="NA", description="Province/State")
    postal_code: Optional[str] = Field(default=None, example="80071", description="Postal code")
    country: Optional[str] = Field(default=None, example="ITA", description="Country")
    
    @model_validator(mode='before')
    def validateUserInfoRequest(cls, user: dict):
        validateBody(cls, user)
        return user
      
    

class UserLoginRequest(BaseModel):
    username: str = Field(..., example="john_doe", description="User's username")
    password: str = Field(..., example="securePass123!", description="User's password")

    @model_validator(mode='before')
    def validateUserRegisterRequest(cls, user: dict):
        validateBody(cls, user)
        return user



class TokenRefreshRequest(BaseModel):
    refresh_token: str = Field(..., example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...", description="Valid refresh token")


class UserRegisterRequest(BaseModel):   
    userCredentials: UserLoginRequest = Field(..., description="User login credentials")
    userInfo: UserInfoRequest = Field(..., description="User personal information")

    @model_validator(mode='before')
    def validateUserRegisterRequest(cls, user: dict):
        validateBody(cls, user)
        return user
    




