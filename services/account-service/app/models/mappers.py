import uuid
from app.models.db_models import Account, AccountType
from app.models.request_models import AccountCreateRequest
from app.models.response_models import AccountResponse, AccountTypeResponse

def map_account_create_to_db(request: AccountCreateRequest) -> Account:
    # Generate an IBAN-like account number or UUID-based identifier
    account_number = f"ACCT-{uuid.uuid4().hex[:20].upper()}"

    return Account(
        username=request.username,
        user_id=request.user_id,
        account_number=account_number,
        account_type=request.account_type,
        currency=request.currency,
        balance=request.initial_deposit or 0.00,
        available_balance=request.initial_deposit or 0.00,
        credit_limit=request.credit_limit or 0.00,
        interest_rate=request.interest_rate or 0.00,
        is_joint=request.is_joint or False,
        branch_code=request.branch_code,
        product_code=request.product_code
    )


def map_account_db_to_response(db_account: Account) -> AccountResponse:
    return AccountResponse.model_validate(db_account)

def map_account_type_db_to_response(db_account_type: AccountType) -> AccountTypeResponse:
    return AccountTypeResponse.model_validate(db_account_type)