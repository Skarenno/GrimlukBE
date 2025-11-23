from pydantic import BaseModel, Field, ConfigDict, constr
from datetime import datetime
from typing import Optional

class CardResponse(BaseModel):
    id: int
    user_id: int
    account_id: int

    cardholder_name: str
    card_type: str = Field(..., description="debit / credit / prepaid")
    network: Optional[str] = Field(None, description="Visa, MasterCard, Amex, etc.")
    issuer: Optional[str] = Field(None, description="Bank or institution name")

    card_number: str
    last4: constr(min_length=4, max_length=4)  # type: ignore[valid-type]
    masked_number: Optional[str] = Field(None, example="**** **** **** 1234")
    expiry_month: int = Field(..., ge=1, le=12)
    expiry_year: int = Field(..., ge=2023, le=2100)

    status: str = Field("active", description="active / blocked / expired / lost")
    is_virtual: bool = True
    contactless_enabled: bool = True
    daily_limit: float = Field(0.00, ge=0)
    online_payments_enabled: bool = True

    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    last_used_at: Optional[datetime]

    account_id: int
    
    model_config = ConfigDict(from_attributes=True)