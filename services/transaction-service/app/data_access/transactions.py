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


def update_transaction(transaction:Transaction):
    with SessionLocal() as db:
        merged = db.merge(transaction)
        db.commit()
        db.refresh(merged)

    return merged

def get_transaction_by_id(id:int):
    with SessionLocal() as db:
        return db.query(Transaction).filter(Transaction.id == id).first()

def get_transactions_by_user_id(user_id:int):
    with SessionLocal() as db:
        return db.query(Transaction).filter(Transaction.user_id == user_id).all()
