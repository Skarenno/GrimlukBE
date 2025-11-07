from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional

class AccountResponse(BaseModel):
    id: int
    user_id: int
    username: str
    account_number: str
    account_type: str
    currency: str
    balance: Decimal
    available_balance: Decimal
    credit_limit: Decimal
    interest_rate: Decimal
    is_joint: bool
    branch_code: Optional[str] = None
    product_code: Optional[str] = None
    status: str
    opened_at: datetime
    last_activity: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class AccountTypeResponse(BaseModel):
    code: str
    name: str

    model_config = ConfigDict(from_attributes=True)
