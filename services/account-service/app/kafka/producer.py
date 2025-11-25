import json
import logging
from confluent_kafka import Producer, KafkaError
import os 

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

KAFKA_SERVER = os.getenv("KAFKA_SERVER")

class KafkaProducer:
    def __init__(self):
        self.producer = Producer({
            "bootstrap.servers": KAFKA_SERVER
        })
        logger.info("Kafka producer initialized.")

    def delivery_report(self, err, msg):
        if err is not None:
            logger.error(f"❌ Delivery failed: {err}")
        else:
            logger.info(f"📨 Message delivered to {msg.topic()} [{msg.partition()}] offset={msg.offset()}")

    def send(self, topic: str, value: dict | str):

        if isinstance(value, dict):
            try:
                value = json.dumps(value).encode("utf-8")
            except Exception as e:
                logger.error(f"Error encoding JSON for producer: {e}")
                return

        elif isinstance(value, str):
            value = value.encode("utf-8")

        try:
            self.producer.produce(
                topic=topic,
                value=value,
                callback=self.delivery_report
            )
            self.producer.poll(0)  
            logger.info("Message produced")
        except BufferError:
            logger.warning("Producer buffer full, flushing…")
            self.producer.flush()
        except Exception as e:
            logger.error(f"Unexpected error producing Kafka message: {e}")

    def flush(self):
        logger.info("Flushing Kafka producer...")
        self.producer.flush()
        logger.info("Producer flush complete.")
