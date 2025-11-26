
from decimal import Decimal
from fastapi import HTTPException, status
from pydantic import BaseModel, model_validator
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
        if(transaction.get("is_external") == False):
            var_receiving_account_id = transaction.get("r_account_id")
            if(not var_receiving_account_id or var_receiving_account_id == 0):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Not a valid receiving account"
                )

        validateBody(cls, transaction)
        return transaction

class TransactionAccountGetRequest(BaseModel):
    user_id:int
    account_numbers: list[str]

def validateBody(cls, body:dict):
    allowed_keys = cls.model_fields.keys()
    body_keys =  body.keys()

    logger.info(allowed_keys)
    logger.info(body)

    #Check for valid keys
    for attribute in body_keys:
        logger.info(f"attribute: {attribute}")
        if not attribute in allowed_keys:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{attribute} is not a valid key for {cls.__name__}"
            )

