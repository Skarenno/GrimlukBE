import os
from fastapi import Depends
from app.models.request_models import *
from app.services.user_service import *
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker

DB_URL = os.getenv("DATABASE_URL")
db_engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=db_engine)

def open_db():
    db = SessionLocal()       
    try:
        yield db              
    finally:
        db.close()  


def add_access_log(log: UserAccessLogModel):
    with SessionLocal() as db:
        db.add(log)
        db.commit()