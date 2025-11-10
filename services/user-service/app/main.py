import os
from fastapi import FastAPI, APIRouter, Request 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.models.request_models import UserInfoRequest, UserLoginRequest, UserRegisterRequest
from app.models.response_models import *
from app.services.user_service import *
from app.utils.authentication import verify_JWT, check_jwt_user_auth 
from app.exceptions.authentication_exception import *
from jose import JWTError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


app = FastAPI()
user_router = APIRouter(prefix="/user")



@app.options("/health")
def health_check():
    return {"status": "ok"}





@user_router.post("/login")
async def login(user_request: UserLoginRequest, request:Request):
    
    try: 
        ip_address = request.client.host
        (jwt_token, refresh_token, user) = login_user_service(user_request, ip_address)
    except (UserDoesNotExistError, PasswordInvalidError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content= {"detail" : "Invalid username or password"}
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"jwt_token" : jwt_token, 
                  "refresh_token" : refresh_token,
                  "user" : jsonable_encoder(user),
                  "message" : f"User {user_request.username} logged in successfully"}
    )

@user_router.post("/register")
async def register(register_request: UserRegisterRequest):

    try:
        (jwt_token, refresh_token) = register_user_service(register_request.userCredentials)
        user = upsert_user_info_service(register_request.userInfo )
    except UserAlreadyExistsError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": f"User {register_request.userCredentials.username} already registered"}
        )
    
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content= {"jwt_token" : jwt_token, 
                      "refresh_token" : refresh_token,
                      "user" : jsonable_encoder(user),
                      "message" : f"User {register_request.userCredentials.username} regestered successfully"}
        )

@user_router.post("/updateUserInfo")
async def update_user_info(update_user_request: UserInfoRequest, request:Request):
    try:
        check_jwt_user_auth(request.state.user, update_user_request.username)
        upsert_user_info_service(update_user_request)
    except UserDoesNotExistError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
             content={"detail":f"User {update_user_request.username} not found"}
        )
    except JwtPermissionError:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail" : "Authorization error: cannot query other users"}
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail" : f"{update_user_request.username} updated correctly"}
    )

@user_router.get("/getUserInfo/{user_id}", response_model=UserInfoResponse)
async def get_user_info(user_id:int, request:Request):
    try:
        user = get_user_info_service(user_id)
        check_jwt_user_auth(request.state.user, user.username)
    except UserDoesNotExistError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
             content={"detail":f"User {user_id} not found"}
        )
    except JwtPermissionError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail" : "Authorization error: cannot query other users"}
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(user)
    )

@app.middleware('http')
async def middleware(request: Request, call_next):
    free_paths = ["/user/login", "/user/register", "/health"]

    
    if(not request.url.path in free_paths):
        try:
            jwt_payload = verify_JWT(request)
            request.state.user = jwt_payload
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
        
origins = [
"http://localhost:5173",  
"http://127.0.0.1:5173", 
"http://localhost:4173",  
"http://127.0.0.1:4173",  
"http://account-service:8002"

]       


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,         
    allow_methods=["*"],            
    allow_headers=["*"],            
)

app.include_router(user_router) 