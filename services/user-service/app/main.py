import os
from fastapi import FastAPI, APIRouter, Request 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.models.request_models import *
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
        jwt_token = login_user_service(user_request, ip_address)
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
async def register(register_request: UserRegisterRequest):

    try:
        jwt_token = register_user_service(register_request)
    except UserAlreadyExistsError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": f"User {register_request.email} already registered"}
        )
    
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content= {"jwt_token" : jwt_token, "message" : f"User {register_request.email} regestered successfully"}
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

@user_router.get("/getUserInfo/{username}", response_model=UserInfoResponse)
async def get_user_info(username:str, request:Request):
    try:
        check_jwt_user_auth(request.state.user, username)
        user = get_user_info_service(username)
    except UserDoesNotExistError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
             content={"detail":f"User {username} not found"}
        )
    except JwtPermissionError:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail" : "Authorization error: cannot query other users"}
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(user)
    )

@app.middleware('http')
async def middleware(request: Request, call_next):
    free_paths = ["/user/login", "/user/register"]

    
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
    "http://localhost:5173",  # Your frontend URL
    "http://127.0.0.1:5173",  # Sometimes Vite uses 127.0.0.1
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allows requests from these origins
    allow_credentials=True,         # Needed if you send cookies or auth
    allow_methods=["*"],            # Allows POST, GET, OPTIONS, etc.
    allow_headers=["*"],            # Allows custom headers like Authorization
)

app.include_router(user_router) 