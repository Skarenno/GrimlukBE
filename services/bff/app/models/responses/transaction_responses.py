from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class SuccessResponse(BaseModel):
    message: str = Field(..., example="Transaction created successfully", description="Success message")

class TransactionResponse(BaseModel):
    id: int = Field(..., example=12345, description="Unique transaction ID")
    s_account_number: Optional[str] = Field(default=None, example="123456789012", description="Source account number")
    r_account_number: Optional[str] = Field(default=None, example="987654321098", description="Recipient account number")
    amount: Decimal = Field(..., example=150.75, description="Transaction amount")
    created_at: datetime = Field(..., example="2023-12-01T14:30:00Z", description="Transaction creation timestamp")
    status: Optional[str] = Field(default=None, example="completed", description="Transaction status")
    description: Optional[str] = Field(default=None, example="Payment for services", description="Transaction description")
    reject_reason: Optional[str] = Field(default=None, example="Insufficient funds", description="Reason for rejection if applicable")
    is_internal: Optional[bool] = Field(default=None, example=True, description="Whether this is an internal bank transfer")
    is_same_user: Optional[bool] = Field(default=None, example=False, description="Whether source and recipient belong to same user")
    is_blocking_account: Optional[bool] = Field(default=None, example=False, description="Whether the account was blocked after transaction")
    direction: Optional[str] = Field(default=None, example="debit", description="Transaction direction (debit/credit)")

    model_config = ConfigDict(from_attributes=True)

