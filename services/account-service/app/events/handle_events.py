
from app.events.handle_transaction_events import handle_transaction_pending
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def handle_event(topic: str, payload: dict):
    event_name = payload.get("event_name")

    match event_name:
        case "transaction.created":
            handle_transaction_pending(payload)
        case _:
            logger.warning(f"Unhandled event: {event_name}")
