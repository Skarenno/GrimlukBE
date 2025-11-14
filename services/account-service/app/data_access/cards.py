import os
from app.models.db_models import  Card
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

def get_cards_by_user_id(user_id:int):
    with SessionLocal() as db:
        return db.query(Card).filter(Card.user_id == user_id).all()
    
def insert_card(card:Card):
    with SessionLocal() as db:
        if card in db:
            raise KeyError
        
        db.add(card)
        db.commit()
        db.refresh(card)

    return card
