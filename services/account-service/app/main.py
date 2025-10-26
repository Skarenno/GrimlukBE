from fastapi import FastAPI, APIRouter, Request 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import status
from app.models.request_models import *
from app.models.response_models import *
from app.services.account_service import create_account_service
from app.utils.authentication import verify_JWT
from app.exceptions.authentication_exception import *
from app.exceptions.service_exception import *
from jose import JWTError


app = FastAPI()
account_router = APIRouter(prefix="/account")

@app.options("/health")
def health_check():
    return {"status": "ok"}
    

@account_router.post("/create", response_model=AccountResponse)
def create_account(account_create_request:AccountCreateRequest, request:Request):
    try:
        bearer_token = request.headers.get("Authorization")
        user = request.state.user
        account = create_account_service(account_create_request, user, bearer_token)
    except JwtPermissionError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error" : "Authorization error: cannot create for other users"}
        )
    except UserDoesNotExistError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error" : "Authorization error: user does not exist"}
        ) 
    except UserServiceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error" : "Service error: cannot retrieve user information"}
        ) 
    except AccountLimitError:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"error" : "Account error: account limit reached for user"}
        ) 
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error" : "Generic server error"}
        ) 
    
    return account


@app.middleware('http')
async def middleware(request: Request, call_next):
    free_paths = []
    
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

app.include_router(account_router) 