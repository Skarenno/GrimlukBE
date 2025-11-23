import uuid
import random
from datetime import datetime
from app.models.db_models import Account, AccountType, Card, BranchCode
from app.models.request_models import AccountCreateRequest, CardCreateRequest
from app.models.response_models import AccountResponse, AccountTypeResponse, CardResponse, BranchCodeResponse

def map_account_create_to_db(request: AccountCreateRequest) -> Account:
    account_number = f"IT00-{uuid.uuid4().hex[:20].upper()}"

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



def map_card_create_to_db(request: CardCreateRequest) -> Card:
    generated_number = "".join(str(random.randint(0, 9)) for _ in range(16))
    last4 = generated_number[-4:]

    now = datetime.now()
    expiry_month = random.randint(1, 12)
    expiry_year = now.year + 3

    return Card(
        user_id=request.user_id,
        account_id=request.account_id,
        
        cardholder_name=request.cardholder_name,
        card_type=request.card_type,
        network=request.network,
        issuer="Grimluk Banking",   
        
        card_number = generated_number,
        last4=last4,
        expiry_month=expiry_month,
        expiry_year=expiry_year,

        daily_limit=request.daily_limit or 0.00,
        online_payments_enabled=request.online_payments_enabled,

        status="active",
        
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def map_account_db_to_response(db_account: Account) -> AccountResponse:
    return AccountResponse.model_validate(db_account)

def map_account_type_db_to_response(db_account_type: AccountType) -> AccountTypeResponse:
    return AccountTypeResponse.model_validate(db_account_type)

def map_branch_codes_db_to_response(db_branch_code: BranchCode) -> BranchCodeResponse:
    return BranchCodeResponse.model_validate(db_branch_code)

def map_card_db_to_response(db_card: Card) -> CardResponse:
    return CardResponse.model_validate(db_card)