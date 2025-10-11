from pydantic import BaseModel
from app.utils.enum_utils import GENDER

class UserInfoResponse(BaseModel):

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

    class Config:
        from_attributes = True 

    