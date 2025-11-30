from app.kafka.producer import KafkaProducer
from app.events.schemas import TransactionCreatedEvent, TransactionRequestedEvent, TransactionValidatedEvent, TransactionRejectedEvent, RollbackAccountBlockingEvent
from app.kafka.topics import TRANSACTION_PENDING, ROLLBACK_ACCOUNT_BLOCK
from app.data_access.transactions import insert_transaction, update_transaction, get_transaction_by_id
from app.models.mappers import map_request_transaction_event_to_db
from app.core.exceptions.service_exception import TransactionError
from app.models.db_models import Transaction
from app.utils.enum_utils import TRANSACTION_STATUS
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
        is_internal=transaction.is_internal,
        is_blocking=transaction.is_blocking_account,
        is_same_user=transaction.is_same_user
    )

    kafka_producer.send(TRANSACTION_PENDING, event.model_dump_json())
    
    return

def publish_rollback_account_blocking(transaction:Transaction):
    event = RollbackAccountBlockingEvent(
        account_id=transaction.s_account_id
    )
    
    kafka_producer.send(ROLLBACK_ACCOUNT_BLOCK, event.model_dump_json())



def handle_transaction_requested(payload:dict):
    event = TransactionRequestedEvent(**payload)
    logger.info(f"INSERTING TRANSACTION DB FOR EVENT {event.event_name}")
    transaction = insert_transaction(map_request_transaction_event_to_db(event))

    if not transaction:
        logger.info(f"COULD NOT INSERT TRANSACTION DB FOR EVENT {event.event_name}")
        raise TransactionError
    
    publish_transaction_pending(transaction=transaction, user_id=event.user_id)

def handle_transaction_rejected(payload:dict):
    event = TransactionRejectedEvent(**payload)
    db_transaction = get_transaction_by_id(event.transaction_id)

    if not db_transaction:
        logger.error(f"NO TRANSACTION WITH ID {event.transaction_id} FOUND")
        return
    
    db_transaction.status = TRANSACTION_STATUS.REJECTED.value
    db_transaction.reject_reason = event.reason

    logging.info(f"UPDATING TRANSACTION {event.transaction_id} WITH REFECTED STATE")
    if(db_transaction.is_blocking_account):
        publish_rollback_account_blocking(db_transaction)
        
    updated = update_transaction(db_transaction)




def handle_transaction_validated(payload:dict):
    event = TransactionValidatedEvent(**payload)
    db_transaction = get_transaction_by_id(event.transaction_id)

    if not db_transaction:
        logger.error(f"NO TRANSACTION WITH ID {event.transaction_id} FOUND")
        return
    
    db_transaction.status = TRANSACTION_STATUS.VALIDATED.value
    logging.info(f"UPDATING TRANSACTION {event.transaction_id} WITH VALIDATED STATE")
    logger.info(f"STATUS = {db_transaction.status}")
    updated = update_transaction(db_transaction)