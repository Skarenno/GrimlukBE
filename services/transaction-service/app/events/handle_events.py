from app.events.handle_transaction_events import handle_transaction_validated, handle_transaction_rejected
import logging
from app.kafka.topics import TRANSACTION_REJECTED, TRASACTION_VALIDATED
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def handle_event(topic: str, payload: dict):
    event_name = payload.get("event_name")

    if event_name == TRANSACTION_REJECTED:
        logger.info("HANDLING TRANSACTION REJECTED")
        handle_transaction_rejected(payload)
    elif event_name == TRASACTION_VALIDATED:
        logger.info("HANDLING TRANSACTION VALIDATED")
        handle_transaction_validated(payload)
    else:
        logger.warning(f"Unhandled event: {event_name}")