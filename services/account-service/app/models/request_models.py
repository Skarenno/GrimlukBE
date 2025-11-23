
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.utils.enums import NetworkTypes
from decimal import Decimal
from app.models.parent_models import AccountBase

class AccountCreateRequest(AccountBase):
    user_id: int
    username: str
    initial_deposit: Optional[Decimal] = Field(default=10.00, example=100.00)

class CardCreateRequest(BaseModel):
    user_id:int
    account_id: int
    cardholder_name:str
    card_type:str
    network: str
    daily_limit:float
    online_payments_enabled:bool

    @field_validator("network")
    @classmethod
    def validate_network(cls, network: str) -> str:
        if network not in NetworkTypes.__members__:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Network is not valid"
            )

        return network
    
    @field_validator("daily_limit")
    @classmethod
    def validate_daily_limi(cls, daily_limit: float) -> float:
        if daily_limit < 500: 
            if daily_limit <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Daily limit is not valid"
                )
        
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Daily limit must be 500 or higher"
            )
        

        return daily_limit


class CardUpdateRequest(BaseModel):
    daily_limit:float | None = None
    online_payments_enabled:bool |  None = None
    status: str |  None = None

    @field_validator("daily_limit")
    @classmethod
    def validate_daily_limit(cls, daily_limit: float | None) -> float | None:
        if daily_limit is not None:
            if daily_limit <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Daily limit is not valid"
                )
        return daily_limit
    
class DeleteAccountRequest(BaseModel):
    deleteId:int
    transferId:int | None = None