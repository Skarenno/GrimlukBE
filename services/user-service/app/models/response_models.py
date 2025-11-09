from datetime import datetime
from pydantic import BaseModel
from typing import Literal

# Assuming GENDER is an enum like this:
GENDER = Literal["M", "F", "O"]

class UserInfoResponse(BaseModel):
    id: int
    username: str
    tax_code: str
    name: str
    surname: str
    phone: str | None = None
    gender: GENDER | None = None            
    residence_address_1: str | None = None  
    residence_address_2: str | None = None
    birth_date:datetime
    city: str | None = None
    province: str | None = None
    postal_code: str | None = None
    country: str | None = None

    class Config:
        from_attributes = True 

    