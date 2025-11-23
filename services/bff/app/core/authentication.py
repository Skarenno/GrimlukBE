from fastapi import HTTPException, Request, status, Header
from jose import  JWTError, jwt
from passlib.context import CryptContext
from app.core.exceptions.authentication_exceptions import JwtPermissionError
import os

SECRET_KEY = os.getenv("JWT_KEY")
ISSUER = os.getenv("JWT_ISSUER")


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    
def get_current_user(request: Request):
    try:
        payload = verify_JWT(request)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or missing JWT")

def get_jwt_from_request(authorization: str = Header(None)) -> str:

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )

    if authorization.startswith("Bearer "):
        token = authorization.strip()
    else:
        raise JwtPermissionError

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format"
        )

    return token
