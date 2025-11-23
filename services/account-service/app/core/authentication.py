from fastapi import HTTPException, Request
from jose import JWTError, jwt
from app.core.exceptions.authentication_exception import JwtPermissionError
import os

SECRET_KEY = os.getenv("JWT_KEY")
ISSUER = os.getenv("JWT_ISSUER")


ALGORITHM = "HS256"


def verify_JWT(request: Request):
    bearer_token = request.headers.get("Authorization")
    
    if(not bearer_token or not bearer_token.startswith("Bearer ")):
        raise JWTError
    
    
    jwt_token = bearer_token.split(" ")[1]
    jwt_payload = jwt.decode(jwt_token, SECRET_KEY, ALGORITHM)
    
    request.state.user = jwt_payload

    return jwt_payload

def check_jwt_user_auth(jwt_payload:dict, user_id:int):
    user = jwt_payload.get("id")
    if (user != user_id):
        raise JwtPermissionError
    
def get_current_user(request: Request):
    try:
        payload = verify_JWT(request)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or missing JWT")