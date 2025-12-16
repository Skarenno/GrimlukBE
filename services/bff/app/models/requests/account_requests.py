
from pydantic import BaseModel, Field, model_validator
from typing import Optional
from app.models.requests.request_validate_utils import validateBody

    
class AccountCreateRequest(BaseModel):
    account_type: str = Field(..., example="checking", description="Type of account (e.g., checking, savings)")
    currency: str = Field(default="EUR", example="EUR", description="Account currency code")
    credit_limit: Optional[float] = Field(default=1200.00, example=500.00, description="Credit limit for credit accounts")
    interest_rate: Optional[float] = Field(default=2.20, example=1.25, description="Annual interest rate percentage")
    is_joint: Optional[bool] = Field(default=False, example=False, description="Whether the account is joint")
    branch_code: Optional[str] = Field(default=None, example="BR001", description="Branch code for the account")
    product_code: Optional[str] = Field(default=None, example="STDCHK", description="Product code for the account type")
    user_id: int = Field(..., example=12345, description="ID of the user creating the account")
    username: str = Field(..., example="john_doe", description="Username of the account holder")
    initial_deposit: Optional[float] = Field(default=10.00, example=100.00, description="Initial deposit amount")

    @model_validator(mode='before')
    def validateAccountCreate(cls, user: dict):
        validateBody(cls, user)
        return user
    
class DeleteAccountRequest(BaseModel):
    deleteId: int = Field(..., example=123, description="ID of the account to delete")
    transferId: Optional[int] = Field(default=None, example=456, description="ID of account to transfer remaining balance to")
    userId: int = Field(..., example=12345, description="ID of the user requesting deletion")
    
    @model_validator(mode='before')
    def validateAccountDelete(cls, user: dict):
        validateBody(cls, user)
        return user