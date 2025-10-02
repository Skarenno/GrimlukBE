from fastapi import FastAPI, APIRouter, Depends
from app.requests import *
from app.dbClasses import UserCredentials
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
import os
from app.authentication import hash_password, verify_password, create_access_token

app = FastAPI()
user_router = APIRouter(prefix="/user")

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


@user_router.post("/login")
def login(user: UserLoginRequest, db: Session = Depends(open_db)):
      
    db_user = db.query(UserCredentials).filter(UserCredentials.username == user.username).first()

    if(not db_user or not verify_password(user.password, db_user.password)):
        return {"error": "Invalid username or password"}
        
        
        
    return {"message": f"User {user.username} logged in successfully"}

@user_router.post("/register")
def register(request: UserRegisterRequest, db: Session = Depends(open_db)):
    db_user = db.query(UserCredentials).filter(UserCredentials.username == request.username).first()

    if(db_user and db_user.username):
        return {"message" : f"User {request.username} already registered"};
    

    register_user = UserCredentials(
        username=request.username,
        password=hash_password(request.password)
    )

    db.add(register_user)
    db.commit()
    db.refresh(register_user) 
    return {"status": "ok"}


app.include_router(user_router) 