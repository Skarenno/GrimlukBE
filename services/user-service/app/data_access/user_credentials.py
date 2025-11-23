import os
from app.models.db_models import UserCredentialsModel
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

def get_user_credentials_by_username(username:str):
        with SessionLocal() as db:
            return db.query(UserCredentialsModel).filter(UserCredentialsModel.username == username).first()

def add_user_credentials(user: UserCredentialsModel):
    with SessionLocal() as db:
        db.add(user)
        db.commit()
        db.refresh(user)

    return user

