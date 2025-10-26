from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
import re
import logging
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class AccountBase(BaseModel):
    account_type: str = Field(..., example="checking")
    currency: str = Field(default="EUR", example="EUR")
    credit_limit: Optional[Decimal] = Field(default=0.00, example=500.00)
    interest_rate: Optional[Decimal] = Field(default=0.00, example=1.25)
    is_joint: Optional[bool] = False
    branch_code: Optional[str] = None
    product_code: Optional[str] = None
