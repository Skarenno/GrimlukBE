
from pydantic import BaseModel, Field, model_validator
from typing import Optional
from app.models.requests.request_validate_utils import validateBody

    
class AccountCreateRequest(BaseModel):
    account_type: str = Field(..., example="checking")
    currency: str = Field(default="EUR", example="EUR")
    credit_limit: Optional[float] = Field(default=0.00, example=500.00)
    interest_rate: Optional[float] = Field(default=0.00, example=1.25)
    is_joint: Optional[bool] = False
    branch_code: Optional[str] = None
    product_code: Optional[str] = None
    user_id: int
    username: str
    initial_deposit: Optional[float] = Field(default=10.00, example=100.00)

    @model_validator(mode='before')
    def validateAccountCreate(cls, user: dict):
        validateBody(cls, user)
        return user
    
class DeleteAccountRequest(BaseModel):
    deleteId:int
    transferId:int | None = None

    @model_validator(mode='before')
    def validateAccountDelete(cls, user: dict):
        validateBody(cls, user)
        return user