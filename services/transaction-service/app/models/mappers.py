from decimal import Decimal
from app.models.db_models import Transaction  # adjust import to your structure
from app.models.request_models import TransactionCreateRequest

def map_transaction_create_to_db(req: TransactionCreateRequest) -> Transaction:
    return Transaction(
        s_account_id=req.s_account_id,
        r_account_id=req.r_account_id,
        s_account_number=req.sending_account_number,
        r_account_number=req.r_account_number,
        amount=Decimal(str(req.amount)),  
        description=req.description
    )
