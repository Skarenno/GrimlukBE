import os
from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from app.requests import *
from app.dbClasses import UserCredentials
from app.authentication import hash_password, verify_password, generate_jwt, verify_JWT 
from jose import JWTError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


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
async def login(user: UserLoginRequest, db: Session = Depends(open_db)):
      
    db_user = db.query(UserCredentials).filter(UserCredentials.username == user.username).first()

    if(not db_user or not verify_password(user.password, db_user.password)):
        return {"error": "Invalid username or password"}
        
    jwt_token = generate_jwt(username=db_user.username)
        
    return {"token" : jwt_token, "message": f"User {user.username} logged in successfully"}

@user_router.post("/register")
async def register(request: UserRegisterRequest, db: Session = Depends(open_db)):
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

@user_router.post("/user_info")
async def write_user_info(request: UserInfoRequest, db: Session = Depends(open_db)):
    return 1


@app.middleware('http')
async def middleware(request: Request, call_next):
    free_paths = ["/user/login", "/user/register"]

    
    if(not request.url.path in free_paths):
        try:
            verify_JWT(request)
        except JWTError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content= {"detail" : "Token is not valid"}
            )
        except:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content= {"detail" : "Error while decoding token"}
            )
    
    try:
        return await call_next(request)
    except Exception as e:
        print("Unexpected error:", e)
        
        



app.include_router(user_router) 