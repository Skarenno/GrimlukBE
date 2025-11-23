from pydantic import BaseModel, field_validator, model_validator, model_serializer
from fastapi import HTTPException, status
from app.models.requests.request_validate_utils import validateBody
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class UserInfoRequest(BaseModel) : 
    id:int | None = None
    username: str
    tax_code: str
    name : str
    surname: str
    birth_date:str
    phone: str | None = None
    gender: str | None = None
    residence_address_1 : str | None = None
    residence_address_2 : str | None = None
    city : str | None = None
    province : str | None = None
    postal_code: str | None = None
    country: str | None = None
    
    @model_validator(mode='before')
    def validateUserInfoRequest(cls, user: dict):
        validateBody(cls, user)
        return user
      
    

class UserLoginRequest(BaseModel):
    username: str
    password: str

    @model_validator(mode='before')
    def validateUserRegisterRequest(cls, user: dict):
        validateBody(cls, user)
        return user



class TokenRefreshRequest(BaseModel):
    refresh_token:str


class UserRegisterRequest(BaseModel):   
    userCredentials:UserLoginRequest
    userInfo:UserInfoRequest

    @model_validator(mode='before')
    def validateUserRegisterRequest(cls, user: dict):
        validateBody(cls, user)
        return user
    




