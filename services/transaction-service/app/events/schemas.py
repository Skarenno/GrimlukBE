from pydantic import BaseModel
from datetime import datetime

class BaseEvent(BaseModel):
    event_type: str
    timestamp: datetime
    data: dict


class AccountCreatedEvent(BaseEvent):
    class Data(BaseModel):
        account_id: int
        user_id: int
        account_type: str
        currency: str
        created_at: datetime
    
    data: Data


class TransactionCreatedEvent(BaseEvent):
    class Data(BaseModel):
        transaction_id: int
        account_id: int
        amount: float
        currency: str
        merchant: str | None
        method: str
        card_id: int | None
        status: str
        timestamp: datetime
    
    data: Data
