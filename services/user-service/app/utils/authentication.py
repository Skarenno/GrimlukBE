from datetime import datetime, timedelta
from fastapi import Request
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.exceptions.authentication_exception import JwtPermissionError
import os

SECRET_KEY = os.getenv("JWT_KEY")
ISSUER = os.getenv("JWT_ISSUER")


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def generate_jwt(username: str):
    user_data = {
        "sub" : username,
        "iss" : ISSUER
    }
    return (create_access_token(user_data), create_access_token(user_data, expires_delta=timedelta(minutes=480)))

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_JWT(request: Request):
    bearer_token = request.headers.get("Authorization")
    
    if(not bearer_token or not bearer_token.startswith("Bearer ")):
        raise JWTError
    
    
    jwt_token = bearer_token.split(" ")[1]
    jwt_payload = jwt.decode(jwt_token, SECRET_KEY, ALGORITHM)
    
    request.state.user = jwt_payload

    return jwt_payload

def check_jwt_user_auth(jwt_payload:dict, username:str):
    user = jwt_payload.get("sub")
    if (user != username):
        raise JwtPermissionError
