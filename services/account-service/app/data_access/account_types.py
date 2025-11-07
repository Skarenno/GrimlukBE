import os
from fastapi import Depends
from app.models.request_models import *
from app.models.db_models import Account, AccountType
from app.exceptions.authentication_exception import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DB_URL = os.getenv("DATABASE_URL")
db_engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=db_engine)

def open_db():
    db = SessionLocal()       
    try:
        yield db              
    finally:
        db.close()  



def get_all_account_types():
    with SessionLocal() as db:
        return db.query(AccountType).all()
