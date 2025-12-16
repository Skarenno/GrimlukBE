from pydantic import BaseModel, Field, ConfigDict, constr
from datetime import datetime
from typing import Optional

class CardResponse(BaseModel):
    id: int = Field(..., example=12345, description="Unique card ID")
    user_id: int = Field(..., example=67890, description="ID of the card owner")
    account_id: int = Field(..., example=11111, description="ID of the linked account")

    cardholder_name: str = Field(..., example="John Doe", description="Name on the card")
    card_type: str = Field(..., example="debit", description="Type of card (debit/credit/prepaid)")
    network: Optional[str] = Field(default=None, example="Visa", description="Card network (Visa, MasterCard, Amex, etc.)")
    issuer: Optional[str] = Field(default=None, example="Grimluk Bank", description="Bank or institution name")

    card_number: str = Field(..., example="4111111111111111", description="Full card number")
    last4: constr(min_length=4, max_length=4) = Field(..., example="1111", description="Last 4 digits of card number")  # type: ignore[valid-type]
    masked_number: Optional[str] = Field(default=None, example="**** **** **** 1111", description="Masked card number for display")
    expiry_month: int = Field(..., example=12, ge=1, le=12, description="Expiry month")
    expiry_year: int = Field(..., example=2028, ge=2023, le=2100, description="Expiry year")

    status: str = Field("active", example="active", description="Card status (active/blocked/expired/lost)")
    is_virtual: bool = Field(..., example=False, description="Whether this is a virtual card")
    contactless_enabled: bool = Field(..., example=True, description="Whether contactless payments are enabled")
    daily_limit: float = Field(..., example=1000.00, ge=0, description="Daily spending limit")
    online_payments_enabled: bool = Field(..., example=True, description="Whether online payments are enabled")

    created_at: Optional[datetime] = Field(default=None, example="2023-01-15T10:30:00Z", description="Card creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, example="2023-12-01T14:20:00Z", description="Last update timestamp")
    last_used_at: Optional[datetime] = Field(default=None, example="2023-12-15T09:15:00Z", description="Last usage timestamp")

    model_config = ConfigDict(from_attributes=True)