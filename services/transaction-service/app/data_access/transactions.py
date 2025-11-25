import os
from app.models.request_models import *
from app.models.db_models import Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv("DATABASE_URL")
db_engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=db_engine)

def open_db():
    db = SessionLocal()       
    try:
        yield db              
    finally:
        db.close()  


def insert_transaction(transaction:Transaction):
    with SessionLocal() as db: 
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

    return transaction

