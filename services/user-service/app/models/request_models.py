from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
import re
import logging
from app.utils.enum_utils import GENDER

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class UserLoginRequest(BaseModel):
    username: str
    password: str

    @model_validator(mode='before')
    def validateUserRegisterRequest(cls, user: dict):
        validateBody(cls, user)
        return user


class UserRegisterRequest(BaseModel):   
    email: str
    password: str

    @model_validator(mode='before')
    def validateUserRegisterRequest(cls, user: dict):
        validateBody(cls, user)
        return user
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, email: str) -> str:
        email_pattern = re.compile(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        )

        if(not email_pattern.match(email)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is not valid"
            )
        
        return email

    
    @field_validator("password")
    @classmethod
    def validatePasswordStrength(cls, password:str) -> str:
        password_pattern = re.compile(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'
        )

        if (not password_pattern.match(password)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must have be at least 8+ characters and have must include at least one of each: lower case, upper case, number, special character"
            )

        return password




class UserInfoRequest(BaseModel) : 
    
    username: str
    tax_code: str
    name : str
    surname: str
    phone: str | None = None
    gender: GENDER
    residence_address_1 : str
    residence_address_2 : str | None = None
    city : str
    province : str 
    postal_code: str
    country: str

    @model_validator(mode='before')
    def validateUserInfoRequest(cls, user: dict):
        validateBody(cls, user)
        return user
    


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
                detail=f"{attribute} is not a valid key"
            )
        
    #Check for mandatory keys
    #for key in mandatory_keys:
    #    if key not in body_keys:
    #        raise HTTPException(
    #            status_code=status.HTTP_400_BAD_REQUEST,
    #            detail=f"missing property {key}"
    #        )