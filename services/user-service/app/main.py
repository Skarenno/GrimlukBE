from fastapi import FastAPI, Depends
from pydantic import BaseModel 
from app.requests import UserLoginRequest, UserRegisterRequest
from app.dbClasses import UserCredentials
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
import os
from app.authentication import hash_password, verify_password, create_access_token

app = FastAPI()

DB_URL = os.getenv("DATABASE_URL")
db_engine = create_engine(DB_URL)
session = sessionmaker(autoflush=False, autocommit=False, bind=db_engine)

def open_db():
    db = session()       
    try:
        yield db              
    finally:
        db.close()  


@app.options("/health")
def health_check():
    return {"status": "ok"}


@app.post("/login")
def login(user: UserLoginRequest, db: Session = Depends(open_db)):
      
    db_user = db.query(UserCredentials).filter(UserCredentials.username == user.username).first()

    if(not user or not verify_password(user.password, db_user.password)):
        return {"error": "Invalid username or password"}
        
        
        
    return {"message": f"User {user.username} logged in successfully"}

@app.post("/register")
def register(request: UserRegisterRequest, db: Session = Depends(open_db)):
    register_user = UserCredentials(
        username=request.username,
        password=hash_password(request.password)
    )

    db.add(register_user)
    db.commit()
    db.refresh(register_user) 
    return {"status": "ok"}
