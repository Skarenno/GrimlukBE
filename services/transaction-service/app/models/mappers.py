from decimal import Decimal
from app.models.db_models import Transaction  # adjust import to your structure
from app.models.request_models import TransactionCreateRequest
from app.models.response_models import TransactionResponse

def map_transaction_create_to_db(req: TransactionCreateRequest) -> Transaction:
    return Transaction(
        s_account_id=req.s_account_id,
        r_account_id=req.r_account_id,
        s_account_number=req.s_account_number,
        r_account_number=req.r_account_number,
        amount=Decimal(str(req.amount)),  
        description=req.description,
        status="PENDING",
        is_external = req.is_external,
        is_blocking_account = req.is_blocking_account,
        s_user_id = req.user_id
    )


def map_transaction_db_to_response(db_transaction:Transaction, user_id:int) -> TransactionResponse:
    direction = "OUT" if db_transaction.s_user_id == user_id else "IN"
    mapped = TransactionResponse.model_validate(db_transaction)
    mapped.direction = direction
    return mapped