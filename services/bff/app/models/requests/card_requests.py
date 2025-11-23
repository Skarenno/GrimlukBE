
from pydantic import BaseModel


class CardCreateRequest(BaseModel):
    user_id:int
    account_id: int
    cardholder_name:str
    card_type:str
    network: str
    daily_limit:float
    online_payments_enabled:bool



class CardUpdateRequest(BaseModel):
    daily_limit:float | None = None
    online_payments_enabled:bool |  None = None
    status: str |  None = None
