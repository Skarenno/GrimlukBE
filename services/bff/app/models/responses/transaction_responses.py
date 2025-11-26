from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict

class SuccessResponse(BaseModel):
    message: str

class TransactionResponse(BaseModel):
    id: int
    s_account_id: Optional[int]
    s_account_number: Optional[str]
    r_account_number: Optional[str]
    amount: Decimal
    created_at: datetime
    status: Optional[str]
    description: Optional[str]
    reject_reason: Optional[str]
    is_external: Optional[bool]
    is_blocking_account: Optional[bool]

    model_config = ConfigDict(from_attributes=True)

