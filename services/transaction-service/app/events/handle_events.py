
from app.events.handle_transaction_events import handle_transaction_validated, handle_transaction_rejected
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def handle_event(topic: str, payload: dict):
    event_name = payload.get("event_name")

    match event_name:
        case "transaction.rejected":
            handle_transaction_rejected(payload)
        case "transaction.validated":
            handle_transaction_validated(payload)
        case _:
            logger.warning(f"Unhandled event: {event_name}")
