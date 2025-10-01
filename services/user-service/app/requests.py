from pydantic import BaseModel

class UserLoginRequest(BaseModel):
    username: str
    password: str

class UserRegisterRequest(BaseModel):   
    username: str
    email: str
    password: str