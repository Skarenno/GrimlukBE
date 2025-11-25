from pydantic import BaseModel
from typing import Optional


class TransactionCreatedEvent(BaseModel):
    transaction_id: int
    user_id: int
    s_account_id: int
    sending_account_number: str
    r_account_id: Optional[int]
    r_account_number: str
    amount: float
    description: Optional[str]
    is_external: bool
