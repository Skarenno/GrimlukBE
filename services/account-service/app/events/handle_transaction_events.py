from app.events.schemas import TransactionCreatedEvent, TransactionValidatedEvent, TransactionRejectedEvent, RollbackAccountBlockingEvent
from app.data_access.account import update_account
from app.utils.enums import AccountStatus
from app.kafka.topics import TRASACTION_VALIDATED, TRANSACTION_REJECTED
from app.data_access.account import get_account_by_id
from app.services.account_service import process_transaction
from app.kafka.producer import KafkaProducer
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

kafka_producer = KafkaProducer()

def handle_transaction_pending(payload:dict):
    event = TransactionCreatedEvent(**payload)

    s_account = get_account_by_id(event.s_account_id)
    r_account = None

    if not s_account:
        logger.error(f"SENDING_ACCOUNT_NOT_FOUND {event.s_account_number} - event {event.event_name}")
        return publish_transaction_rejected(event=event, reason="SENDING_ACCOUNT_NOT_FOUND")
    
    if s_account.account_number != event.s_account_number:
        logger.error(f"SENDING_ACCOUNT_NUMBER_INCORRECT {event.s_account_number} - event {event.event_name}")
        return publish_transaction_rejected(event=event, reason="SENDING_ACCOUNT_NUMBER_INCORRECT")
    
    if s_account.balance < event.amount:
        logger.error(f"NOT_SUFFICIENT_FUNDS {event.amount} - event {event.event_name}")
        return publish_transaction_rejected(event=event, reason="NOT_SUFFICIENT_FUNDS")
    
    if event.amount > s_account.credit_limit:
        logger.error(f"AMOUNT_OVER_LIMIT {s_account.credit_limit} - event {event.event_name}")
        return publish_transaction_rejected(event=event, reason="AMOUNT_OVER_LIMIT")
    
    if event.amount < 0:
        logger.error(f"AMOUNT_INVALID: {event.amount} - event {event.event_name}")
        return publish_transaction_rejected(event=event, reason="AMOUNT_INVALID")  

    if not event.is_external:
        r_account = get_account_by_id(event.r_account_id)
        if not r_account or r_account.account_number != event.r_account_number:
            logger.error(f"RECEIVING_ACCOUNT_NOT_FOUND {event.r_account_number} - event {event.event_name}")
            return publish_transaction_rejected(event=event, reason="RECEIVING_ACCOUNT_NOT_FOUND")
        
        
    try:
        process_transaction(event, s_account, r_account)
    except Exception as e:
        logger.error(f"ACCONT_BALANCING_ERROR {e} - event {event.event_name}")
        return publish_transaction_rejected(event=event, reason="ACCONT_BALANCING_ERROR")

    logger.info(f"PUBLISHING TRANSACTION OK EVENT FROM PENDING {event.transaction_id}")
    publish_transaction_validated(event=event)


def handle_rollback_blocking(payload:dict):
    event = RollbackAccountBlockingEvent(**payload)
    account = get_account_by_id(event.account_id)

    if not account:
        logger.error(f"COULD NOT ROLLBACK ACCOUNT {event.account_id} - ACCOUNT NOT FOUND")
        return
    
    if account.status != AccountStatus.DELETED.value:
        logger.error(f"COULD NOT ROLLBACK ACCOUNT {event.account_id} - ACCOUNT STATUS INVALID")
        return
    
    account.status = AccountStatus.ACTIVE.value
    update_account(account=account)

def publish_transaction_validated(event:TransactionCreatedEvent):
    validated = TransactionValidatedEvent(
        transaction_id=event.transaction_id,
        amount=event.amount,
        s_account_id=event.s_account_id,
        r_account_id=event.r_account_id
    )

    kafka_producer.send(TRASACTION_VALIDATED, validated.model_dump_json())


def publish_transaction_rejected(event:TransactionCreatedEvent, reason:str):
    rejected = TransactionRejectedEvent(
        transaction_id=event.transaction_id,
        amount=event.amount,
        s_account_id=event.s_account_id,
        r_account_id=event.r_account_id,
        reason=reason
    )

    kafka_producer.send(TRANSACTION_REJECTED, rejected.model_dump_json())

