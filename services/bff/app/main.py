from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions.exception_handler import register_exception_handlers
from app.routers.user_router import router as user_router
from app.routers.cards_router import router as card_router
from app.routers.accounts_router import router as account_router


app = FastAPI(
    title="Banking BFF",
    description="Backend-for-Frontend for account, card, user, and transaction services",
    version="1.0.0",
)

register_exception_handlers(app)

@app.get("/health")
def health_check():
    return {"status": "ok"}



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

