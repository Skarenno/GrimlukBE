from fastapi import FastAPI, Request 
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.authentication import verify_JWT
from app.exceptions.authentication_exception import *
from app.exceptions.service_exception import *
from jose import JWTError

from app.routers import accounts, cards


app = FastAPI()

@app.options("/health")
def health_check():
    return {"status": "ok"}
    
app.include_router(accounts.router)
app.include_router(cards.router)


@app.middleware('http')
async def middleware(request: Request, call_next):
    free_paths = ["/health"]
    
    if(not request.url.path in free_paths):
        try:
            jwt_payload = verify_JWT(request)
            request.state.user = jwt_payload
        except JWTError as je:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content= {"error" : "Token is not valid - " + str(je)}
            )
        except:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content= {"error" : "Error while decoding token"}
            )
    
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content= {"error" : "Unexpected error - " + str(e)}
        )
    
origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173", 
    "http://localhost:4173",  
    "http://127.0.0.1:4173",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allows requests from these origins
    allow_credentials=True,         # Needed if you send cookies or auth
    allow_methods=["*"],            # Allows POST, GET, OPTIONS, etc.
    allow_headers=["*"],            # Allows custom headers like Authorization
)

