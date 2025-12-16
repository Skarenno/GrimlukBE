from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional

class AccountResponse(BaseModel):
    id: int = Field(..., example=123, description="Unique account ID")
    user_id: int = Field(..., example=12345, description="ID of the account owner")
    username: str = Field(..., example="john_doe", description="Username of the account holder")
    account_number: str = Field(..., example="123456789012", description="Account number")
    account_type: str = Field(..., example="checking", description="Type of account")
    currency: str = Field(..., example="EUR", description="Account currency")
    balance: Decimal = Field(..., example=1500.50, description="Current account balance")
    available_balance: Decimal = Field(..., example=1450.50, description="Available balance for transactions")
    credit_limit: Decimal = Field(..., example=500.00, description="Credit limit")
    interest_rate: Decimal = Field(..., example=1.25, description="Annual interest rate")
    is_joint: bool = Field(..., example=False, description="Whether the account is joint")
    branch_code: Optional[str] = Field(default=None, example="BR001", description="Branch code")
    product_code: Optional[str] = Field(default=None, example="STDCHK", description="Product code")
    status: str = Field(..., example="active", description="Account status")
    opened_at: datetime = Field(..., example="2023-01-15T10:30:00Z", description="Account opening date")
    last_activity: Optional[datetime] = Field(default=None, example="2023-12-01T14:20:00Z", description="Last activity date")
    created_at: datetime = Field(..., example="2023-01-15T10:30:00Z", description="Record creation date")
    updated_at: Optional[datetime] = Field(default=None, example="2023-12-01T14:20:00Z", description="Last update date")

    model_config = ConfigDict(from_attributes=True)



class AccountTypeResponse(BaseModel):
    code: str = Field(..., example="CHK", description="Account type code")
    name: str = Field(..., example="Checking Account", description="Account type name")

    model_config = ConfigDict(from_attributes=True)


class BranchCodeResponse(BaseModel):
    code: str = Field(..., example="BR001", description="Branch code")
    name: str = Field(..., example="Main Branch", description="Branch name")

    model_config = ConfigDict(from_attributes=True)