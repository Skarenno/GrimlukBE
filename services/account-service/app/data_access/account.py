import os
from fastapi import Depends
from app.models.request_models import *
from app.models.db_models import Account, Card
from app.exceptions.authentication_exception import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DB_URL = os.getenv("DATABASE_URL")
db_engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=db_engine)

def open_db():
    db = SessionLocal()       
    try:
        yield db              
    finally:
        db.close()  


def update_account(account:Account):
    account.updated_at = datetime.now()
    with SessionLocal() as db:
        
        updated = db.merge(account)
        db.commit()
        db.refresh(updated)
        return updated
    
def insert_account(account:Account):
    with SessionLocal() as db:
        
        db.add(account)
        db.commit()
        db.refresh(account)

    return account

def get_accounts_by_userid(user_id:int):
    with SessionLocal() as db:
        return db.query(Account).filter(Account.user_id == user_id).all()

def get_account_by_id(accountid:int): 
    with SessionLocal() as db:
        return db.query(Account).filter(Account.id == accountid).first()