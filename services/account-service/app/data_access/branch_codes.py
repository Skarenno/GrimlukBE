import os
from app.models.request_models import *
from app.models.db_models import BranchCode
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



def get_all_branch_codes():
    with SessionLocal() as db:
        return db.query(BranchCode).all()
