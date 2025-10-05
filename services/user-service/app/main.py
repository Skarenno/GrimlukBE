import os
from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from app.models.request_models import *
from app.services.user_service import *
from app.utils.authentication import verify_JWT 
from jose import JWTError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


app = FastAPI()
user_router = APIRouter(prefix="/user")

DB_URL = os.getenv("DATABASE_URL")
db_engine = create_engine(DB_URL)
session = sessionmaker(autoflush=False, autocommit=False, bind=db_engine)

@app.options("/health")
def health_check():
    return {"status": "ok"}

def open_db():
    db = session()       
    try:
        yield db              
    finally:
        db.close()  



@user_router.post("/login")
async def login(user_request: UserLoginRequest, request:Request, db: Session = Depends(open_db)):
    
    try: 
        ip_address = request.client.host
        jwt_token = login_user_service(user_request, ip_address, db)
    except (UserDoesNotExistError, PasswordInvalidError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content= {"detail" : "Invalid username or password"}
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"jwt_token" : jwt_token, "message" : f"User {user_request.username} logged in successfully"}
    )

@user_router.post("/register")
async def register(register_request: UserRegisterRequest, db: Session = Depends(open_db)):

    try:
        jwt_token = register_user_service(register_request, db)
    except UserAlreadyExistsError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": f"User {register_request.username} already registered"}
        )
    
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content= {"jwt_token" : jwt_token, "message" : f"User {register_request.username} regestered successfully"}
        )

@user_router.post("/update_user_info")
async def update_user_info(update_user_request: UserInfoRequest, db: Session = Depends(open_db)):
    try:
        update_user_info_service(update_user_request, db)
    except UserDoesNotExistError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
             content={"detail":f"User {update_user_request.username} not found"}
        )


    return 1


@app.middleware('http')
async def middleware(request: Request, call_next):
    free_paths = ["/user/login", "/user/register"]

    
    if(not request.url.path in free_paths):
        try:
            verify_JWT(request)
        except JWTError as je:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content= {"detail" : "Token is not valid - " + str(je)}
            )
        except:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content= {"detail" : "Error while decoding token"}
            )
    
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content= {"detail" : "Unexpected error - " + str(e)}
        )
        
        



app.include_router(user_router) 