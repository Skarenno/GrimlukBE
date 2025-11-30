# main.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.authentication import verify_JWT
from jose import JWTError
from app.routers.transaction_router import router as transaction_router
from app.kafka.consumer import KafkaBackgroundConsumer
from app.kafka.topics import TRASACTION_VALIDATED, TRANSACTION_REJECTED
from app.core.exceptions.exception_handler import register_exception_handlers
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="FastAPI + Kafka Microservice",
    version="1.0.0",
)

register_exception_handlers(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Transaction Service",
    version="1.0.0"
)


# Init consumer instance
kafka_consumer = KafkaBackgroundConsumer(
    topics=[TRASACTION_VALIDATED, TRANSACTION_REJECTED]  
)


@app.on_event("startup")
def startup_event():
    logger.info("Starting transaction-service…")
    kafka_consumer.start()
    logger.info("Kafka consumer initialized.")



@app.on_event("shutdown")
def shutdown_event():
    logger.info("Stopping transaction-service…")
    kafka_consumer.stop()
    logger.info("Service shutdown complete.")



@app.options("/health")
def health_check():
    return {"status": "ok"}


app.include_router(transaction_router)


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    free_paths = ["/health"]

    if request.url.path not in free_paths:
        try:
            jwt_payload = verify_JWT(request)
            request.state.user = jwt_payload
        except JWTError as je:
            logger.exception("JWTError at %s %s", request.method, request.url.path, exc_info=je)
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Token is not valid - " + str(je)},
            )
        except Exception as e:
            logger.exception("JWT decode error at %s %s", request.method, request.url.path, exc_info=e)
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Error while decoding token"},
            )
    return await call_next(request)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)