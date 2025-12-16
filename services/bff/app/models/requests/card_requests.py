
from pydantic import BaseModel, Field
from typing import Optional


class CardCreateRequest(BaseModel):
    user_id: int = Field(..., example=12345, description="ID of the user requesting the card")
    account_id: int = Field(..., example=67890, description="ID of the account to link the card to")
    cardholder_name: str = Field(..., example="John Doe", description="Name to appear on the card")
    card_type: str = Field(..., example="debit", description="Type of card (debit/credit)")
    network: str = Field(..., example="visa", description="Card network (visa, mastercard, etc.)")
    daily_limit: float = Field(..., example=1000.00, description="Daily spending limit")
    online_payments_enabled: bool = Field(..., example=True, description="Whether online payments are enabled")



class CardUpdateRequest(BaseModel):
    daily_limit: Optional[float] = Field(default=None, example=1500.00, description="Updated daily spending limit")
    online_payments_enabled: Optional[bool] = Field(default=None, example=False, description="Updated online payments setting")
    status: Optional[str] = Field(default=None, example="blocked", description="Updated card status (active/blocked)")
