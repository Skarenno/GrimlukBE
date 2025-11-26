import os
from app.models.db_models import Transaction
from app.models.request_models import TransactionAccountGetRequest, TransactionCreateRequest
from app.models.response_models import SuccessResponse, TransactionResponse
from app.core.exceptions.service_exception import TransactionError
from app.core.authentication import check_jwt_user_auth
from app.data_access.transactions import insert_transaction, get_transactions_by_user_id, get_transactions_by_account_number
from app.models.mappers import map_transaction_create_to_db, map_transaction_db_to_response
from app.kafka.producer import KafkaProducer
from app.events.handle_transaction_events import publish_transaction_pending

kafka_producer = KafkaProducer()

def create_transaction_service(request:TransactionCreateRequest, jwt_user:dict) -> SuccessResponse:
    check_jwt_user_auth(jwt_payload=jwt_user, user_id=request.user_id)
    transaction = insert_transaction(map_transaction_create_to_db(request))

    if not transaction:
        raise TransactionError
    
    publish_transaction_pending(transaction=transaction, user_id=request.user_id)
    return SuccessResponse(message="Transaction created")

def get_transactions_by_user_id_service(user_id:int, jwt_user:dict) -> list[TransactionResponse]:
    check_jwt_user_auth(jwt_payload=jwt_user, user_id=user_id)
    transactions = get_transactions_by_user_id(user_id)

    return [map_transaction_db_to_response(transaction, user_id=user_id) for transaction in transactions]

def get_transactions_by_account_list_service(transactionRequest: TransactionAccountGetRequest, jwt_user:dict):
    check_jwt_user_auth(jwt_payload=jwt_user, user_id=transactionRequest.user_id)
    transactions : list[Transaction] = []
    
    for account_number in transactionRequest.account_numbers:
        transactions.extend(get_transactions_by_account_number(account_number))

    return [map_transaction_db_to_response(transaction, user_id=transactionRequest.user_id) for transaction in transactions]
