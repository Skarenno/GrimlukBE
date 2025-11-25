# consumer.py
import threading
import logging
import time
from confluent_kafka import Consumer, KafkaException, KafkaError
from app.events.handle_events import handle_event
import os
import json


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

KAFKA_SERVER = os.getenv("KAFKA_SERVER")
GROUP_ID = os.getenv("GROUP_ID")

class KafkaBackgroundConsumer:
    def __init__(self, topics: list[str]):
        self.running = False
        self.topics = topics

        # Your config
        self.consumer = Consumer({
            "bootstrap.servers": KAFKA_SERVER,
            "group.id": GROUP_ID,
            "auto.offset.reset": "earliest"
        })

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._consume_loop, daemon=True)
        self.thread.start()
        logger.info("Kafka consumer background thread started.")

    def stop(self):
        logger.info("Stopping Kafka consumer…")
        self.running = False
        time.sleep(1)  
        try:
            self.consumer.close()
        except Exception as e:
            logger.error(f"Error closing consumer: {e}")

        logger.info("Kafka consumer stopped.")

    def _consume_loop(self):
        logger.info(f"Subscribing to Kafka topics: {self.topics}")
        self.consumer.subscribe(self.topics)

        try:
            while self.running:
                msg = self.consumer.poll(1.0)  

                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue  
                    logger.error(f"Kafka error: {msg.error()}")
                    continue

                self.handle_message(msg)

        except KafkaException as e:
            logger.exception("Kafka exception during consumption.", exc_info=e)
        except Exception as general:
            logger.exception("Unexpected error in consumer thread.", exc_info=general)
        finally:
            logger.info("Closing Kafka consumer...")
            self.consumer.close()

    def handle_message(self, msg):
        try:
            topic = msg.topic()
            decoded_json = json.loads(msg.value().decode("utf-8"))

            logger.info(f"Received from topic '{topic}': {decoded_json}")

            handle_event(topic, decoded_json)

        except Exception as e:
            logger.error(f"Failed to process message: {e}")
