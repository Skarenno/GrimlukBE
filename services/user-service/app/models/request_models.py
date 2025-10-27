from pydantic import BaseModel, field_validator, model_validator, model_serializer
from fastapi import HTTPException, status
import re
import logging
from app.utils.enum_utils import GENDER
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class UserInfoRequest(BaseModel) : 
    id:str
    username: str
    tax_code: str
    name : str
    surname: str
    birth_date:str
    phone: str | None = None
    gender: GENDER | None = None
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
    
    @field_validator("username")
    @classmethod
    def validate_email(cls, mail: str) -> str:
        email_pattern = re.compile(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        )

        if(not email_pattern.match(mail)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is not valid"
            )
        
        return mail
    
    @field_validator("phone")
    def validate_phone(cls, phone:str) -> str:
        phone = re.sub(r"(?!^\+)\D", "", phone)
        return phone
    
    @field_validator("birth_date")
    def validate_birth(cls, birth_date: str) -> str:

        try:
            dt = datetime.strptime(birth_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Birth date must be a valid date"
            )

        if dt > datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Birth date cannot be in the future"
            )

        min_age_years = 18
        if (datetime.now() - dt).days < min_age_years * 365:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"You must be at least {min_age_years} years old to register"
            )

        return birth_date        
    

class UserLoginRequest(BaseModel):
    username: str
    password: str

    @model_validator(mode='before')
    def validateUserRegisterRequest(cls, user: dict):
        validateBody(cls, user)
        return user
    
    @field_validator("username")
    @classmethod
    def validate_email(cls, username: str) -> str:
        email_pattern = re.compile(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        )

        if(not email_pattern.match(username)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is not valid"
            )
        
        return username


class UserRegisterRequest(BaseModel):   
    userCredentials:UserLoginRequest
    userInfo:UserInfoRequest

    @model_validator(mode='before')
    def validateUserRegisterRequest(cls, user: dict):
        validateBody(cls, user)
        return user
    


    
    @field_validator("userCredentials")
    @classmethod
    def validatePasswordStrength(cls, userCredentials:UserLoginRequest) -> UserLoginRequest:
        password = userCredentials.password
        password_pattern = re.compile(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'
        )

        if (not password_pattern.match(password)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must have be at least 8+ characters and have must include at least one of each: lower case, upper case, number, special character"
            )

        return userCredentials


def validateBody(cls, body:dict):
    allowed_keys = cls.model_fields.keys()
    body_keys =  body.keys()

    logger.info(allowed_keys)
    logger.info(body)

    #Check for valid keys
    for attribute in body_keys:
        logger.info(f"attribute: {attribute}")
        if not attribute in allowed_keys:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{attribute} is not a valid key for {cls.__name__}"
            )

    #Check for mandatory keys
    #for key in mandatory_keys:
    #    if key not in body_keys:
    #        raise HTTPException(
    #            status_code=status.HTTP_400_BAD_REQUEST,
    #            detail=f"missing property {key}"
    #        )