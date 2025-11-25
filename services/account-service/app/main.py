from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.exceptions.exception_handler import register_exception_handlers
from app.core.authentication import verify_JWT
from app.kafka.consumer import KafkaBackgroundConsumer
from jose import JWTError
import logging

from app.routers import accounts, cards

logger = logging.getLogger("api-errors")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


sql_logger = logging.getLogger("sqlalchemy.engine")
sql_logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
sql_logger.addHandler(handler)

app = FastAPI()

app.include_router(accounts.router)
app.include_router(cards.router)

register_exception_handlers(app)


@app.options("/health")
def health_check():
    return {"status": "ok"}


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


kafka_consumer = KafkaBackgroundConsumer(
    topics=["transaction.pending"]  
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
