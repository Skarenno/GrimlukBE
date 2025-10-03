from pydantic import BaseModel, EmailStr, field_validator, model_validator
from fastapi import HTTPException, status
import re
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class UserLoginRequest(BaseModel):
    username: str
    password: str

    @model_validator(mode='before')
    def validateUserRegisterRequest(cls, user: dict):
        validateBody(cls, user)

        if(not user["username"] or user["username"].strip() == ""):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username cannot be empty"
            )

        return user

class UserRegisterRequest(BaseModel):   
    username: str
    email: str
    password: str

    @model_validator(mode='before')
    def validateUserRegisterRequest(cls, user: dict):
        validateBody(cls, user)

        if(not user["username"] or user["username"].strip() == "" or not user["email"] or user["email"].strip() == ""):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username cannot be empty"
            )

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


def validateBody(cls, body:dict):
    allowed_keys = cls.model_fields.keys()

    logger.info(allowed_keys)
    for attribute in body.keys:
        logger.info(f"attribute: {attribute}")
        if not attribute in allowed_keys:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username cannot be empty"
            )