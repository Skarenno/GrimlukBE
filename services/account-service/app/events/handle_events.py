from app.events.handle_transaction_events import handle_transaction_pending, handle_rollback_blocking
import logging
from app.kafka.topics import TRANSACTION_PENDING, ROLLBACK_ACCOUNT_BLOCK

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def handle_event(topic: str, payload: dict):
    event_name = payload.get("event_name")

    # Use equality checks instead of match/case for constant comparison
    if event_name == TRANSACTION_PENDING:
        logger.info("HANDLING TRANSACTION PENDING")
        handle_transaction_pending(payload)
    elif event_name == ROLLBACK_ACCOUNT_BLOCK:
        logger.info("HANDLING ACCOUNT ROLLBACK")
        handle_rollback_blocking(payload)
    else:
        logger.warning(f"Unhandled event: {event_name}")