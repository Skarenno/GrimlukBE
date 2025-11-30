from app.events.schemas import TransactionRequestedEvent, TransactionCreatedEvent, TransactionValidatedEvent, TransactionRejectedEvent
from app.kafka.topics import TRANSACTION_REQUEST, TRASACTION_VALIDATED, TRANSACTION_REJECTED
from app.kafka.producer import KafkaProducer
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

kafka_producer = KafkaProducer()

def publish_transaction_validated(event:TransactionCreatedEvent):
    validated = TransactionValidatedEvent(
        transaction_id=event.transaction_id,
        amount=event.amount,
        s_account_id=event.s_account_id,
        r_account_id=event.r_account_id
    )

    kafka_producer.send(TRASACTION_VALIDATED, validated.model_dump_json())


def publish_request_transfer(event:TransactionRequestedEvent):
    kafka_producer.send(TRANSACTION_REQUEST, event.model_dump_json())

def publish_transaction_rejected(event:TransactionCreatedEvent, reason:str):
    rejected = TransactionRejectedEvent(
        transaction_id=event.transaction_id,
        amount=event.amount,
        s_account_id=event.s_account_id,
        r_account_id=event.r_account_id,
        reason=reason
    )

    kafka_producer.send(TRANSACTION_REJECTED, rejected.model_dump_json())