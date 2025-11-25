import os
from app.models.request_models import TransactionCreateRequest
from app.models.response_models import SuccessResponse
from app.core.exceptions.service_exception import TransactionError
from app.core.authentication import check_jwt_user_auth
from app.data_access.transactions import insert_transaction
from app.models.mappers import map_transaction_create_to_db
from app.kafka.producer import KafkaProducer
from app.models.kafka_models import TransactionCreatedEvent

kafka_producer = KafkaProducer()

def create_transaction_service(request:TransactionCreateRequest, jwt_user:dict) -> SuccessResponse:
    check_jwt_user_auth(jwt_payload=jwt_user, user_id=request.user_id)
    transaction = insert_transaction(map_transaction_create_to_db(request))

    if not transaction:
        raise TransactionError
    
    event = TransactionCreatedEvent(
        transaction_id=transaction.id,
        user_id=request.user_id,
        s_account_id=request.s_account_id,
        sending_account_number=request.sending_account_number,
        r_account_id=request.r_account_id,
        r_account_number=request.r_account_number,
        amount=request.amount,
        description=request.description,
        is_external=request.is_external
    )

    kafka_producer.send("transaction.pending", event.model_dump())
    
    return SuccessResponse(message="Transaction created")

