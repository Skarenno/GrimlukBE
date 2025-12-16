
from decimal import Decimal
from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from app.models.requests.request_validate_utils import validateBody
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class TransactionCreateRequest(BaseModel):
    user_id: int = Field(..., example=12345, description="ID of the user initiating the transaction")
    s_account_id: int = Field(..., example=67890, description="ID of the source account")
    s_account_number: str = Field(..., example="1234567890", description="Account number of the source account")
    r_account_id: Optional[int] = Field(default=None, example=54321, description="ID of the recipient account (for internal transfers)")
    r_account_number: str = Field(..., example="0987654321", description="Account number of the recipient account")
    amount: Decimal = Field(..., example=100.50, description="Transaction amount")
    description: Optional[str] = Field(default=None, example="Payment for services", description="Optional transaction description")
    is_internal: bool = Field(..., example=True, description="Whether this is an internal bank transfer")
    is_same_user: bool = Field(..., example=False, description="Whether source and recipient belong to same user")
    is_blocking_account: bool = Field(..., example=False, description="Whether to block the account after transaction")

    
    @model_validator(mode="before")
    def validate_request(cls, transaction: dict):
        validateBody(cls, transaction)
        return transaction


            
class TransactionAccountGetRequest(BaseModel):
    user_id: int = Field(..., example=12345, description="ID of the user requesting transactions")
    account_numbers: List[str] = Field(..., example=["1234567890", "0987654321"], description="List of account numbers to get transactions for")
