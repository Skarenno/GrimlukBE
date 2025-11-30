from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


class TransactionCreatedEvent(BaseModel):
    event_name:str = "transaction.pending"
    transaction_id: int
    user_id: int
    s_account_id: int
    s_account_number: str
    r_account_id: Optional[int]
    r_account_number: str
    amount: Decimal
    description: Optional[str]
    is_internal: bool
    is_same_user:bool

class TransactionValidatedEvent(BaseModel):
    event_name:str = "transaction.validated"
    transaction_id: int
    s_account_id: int
    r_account_id: Optional[int]
    amount: Decimal

class TransactionRejectedEvent(BaseModel):
    event_name:str = "transaction.rejected"
    transaction_id: int
    s_account_id: int
    r_account_id: Optional[int]
    amount: Decimal
    reason:str

class RollbackAccountBlockingEvent(BaseModel):
    event_name:str = "account.rollback"
    account_id:int