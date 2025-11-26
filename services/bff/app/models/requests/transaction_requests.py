
from decimal import Decimal
from pydantic import BaseModel, model_validator
from app.models.requests.request_validate_utils import validateBody
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class TransactionCreateRequest(BaseModel):
    user_id : int
    s_account_id: int
    s_account_number:str
    r_account_id: int | None = None
    r_account_number:str
    amount: Decimal
    description: str | None = None
    is_external:bool
    is_blocking_account:bool

    
    @model_validator(mode="before")
    def validate_request(cls, transaction: dict):
        validateBody(cls, transaction)
        return transaction


            
class TransactionAccountGetRequest(BaseModel):
    user_id:int
    account_numbers: list[str]
