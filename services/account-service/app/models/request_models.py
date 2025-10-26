
from pydantic import Field
from typing import Optional

from decimal import Decimal
from app.models.response_models import AccountResponse
from app.models.parent_models import AccountBase

class AccountCreateRequest(AccountBase):
    user_id: int
    username: str
    initial_deposit: Optional[Decimal] = Field(default=0.00, example=100.00)
