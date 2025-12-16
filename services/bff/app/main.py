from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions.exception_handler import register_exception_handlers
from app.routers.user_router import router as user_router
from app.routers.cards_router import router as card_router
from app.routers.accounts_router import router as account_router
from app.routers.transaction_router import router as transaction_router

app = FastAPI(
    title="Grimluk Banking BFF API",
    description="Backend-for-Frontend service providing unified access to account, card, user, and transaction management in the Grimluk Finance and Banking system. This API aggregates multiple microservices and provides a consistent interface for frontend applications.",
    version="1.0.0",
    contact={
        "name": "Grimluk Development Team",
        "email": "dev@grimluk.com",
        "url": "https://grimluk.com"
    },
    license_info={
        "name": "Proprietary",
        "url": "https://grimluk.com/license"
    }
)

register_exception_handlers(app)

@app.get("/health", summary="Health check", description="Check if the BFF service is running and healthy.")
def health_check():
    return {"status": "ok", "service": "BFF", "version": "1.0.0"}



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(user_router)
app.include_router(account_router)
app.include_router(card_router)
app.include_router(transaction_router)