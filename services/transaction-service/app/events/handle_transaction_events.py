from app.kafka.producer import KafkaProducer
from app.events.schemas import TransactionCreatedEvent, TransactionValidatedEvent, TransactionRejectedEvent
from app.kafka.topics import TRANSACTION_PENDING
from app.data_access.transactions import update_transaction, get_transaction_by_id
from app.models.db_models import Transaction
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


kafka_producer = KafkaProducer()

def publish_transaction_pending(transaction:Transaction, user_id:int):

    event = TransactionCreatedEvent(
        transaction_id=transaction.id,
        user_id=user_id,
        s_account_id=transaction.s_account_id,
        s_account_number=transaction.s_account_number,
        r_account_id=transaction.r_account_id,
        r_account_number=transaction.r_account_number,
        amount=transaction.amount,
        description=transaction.description,
        is_external=transaction.is_external
    )

    kafka_producer.send(TRANSACTION_PENDING, event.model_dump_json())
    
    return



def handle_transaction_rejected(payload:dict):
    event = TransactionRejectedEvent(**payload)
    db_transaction = get_transaction_by_id(event.transaction_id)

    if not db_transaction:
        logger.error(f"NO TRANSACTION WITH ID {event.transaction_id} FOUND")
        return
    
    db_transaction.status = "REJECTED"
    db_transaction.reject_reason = event.reason

    logging.info(f"UPDATING TRANSACTION {event.transaction_id} WITH REFECTED STATE")
    updated = update_transaction(db_transaction)




def handle_transaction_validated(payload:dict):
    event = TransactionValidatedEvent(**payload)
    db_transaction = get_transaction_by_id(event.transaction_id)

    if not db_transaction:
        logger.error(f"NO TRANSACTION WITH ID {event.transaction_id} FOUND")
        return
    
    db_transaction.status = "VALIDATED"
    logging.info(f"UPDATING TRANSACTION {event.transaction_id} WITH VALIDATED STATE")
    logger.info(f"STATUS = {db_transaction.status}")
    updated = update_transaction(db_transaction)