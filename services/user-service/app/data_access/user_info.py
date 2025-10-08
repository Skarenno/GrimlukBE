import os
from fastapi import Depends
from app.models.request_models import *
from app.services.user_service import *
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

def get_user_info_by_username(username:str):
    with SessionLocal() as db:
        return db.query(UserModel).filter(UserModel.username == username).first()


def upsert_user_info(user:UserModel):
    with SessionLocal() as db:
        if user not in db:
            db.add(user)

        db.commit()
        db.refresh(user)
        return user
