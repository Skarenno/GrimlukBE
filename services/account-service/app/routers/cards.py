from fastapi import APIRouter, Request 
from fastapi.responses import JSONResponse
from fastapi import status
from app.models.request_models import *
from app.models.response_models import *
from app.services.card_service import get_cards_service, create_card_service
from app.exceptions.authentication_exception import *
from app.exceptions.service_exception import *


router = APIRouter(prefix="/card")


@router.get("/getByUser/{user_id}", response_model=list[CardResponse])
def get_user_cards_list(user_id: int, request:Request):
    try:
        cards = get_cards_service(user_id)
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error" : "Generic server error"}
        ) 
    
    return cards

@router.post("/create", response_model=CardResponse)
def create_card(createCardRequest:CardCreateRequest, request:Request):
    try:
        bearer_token = request.headers.get("Authorization")
        card = create_card_service(createCardRequest, bearer_token)
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
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error" : "Generic server error"}
        ) 
    
    return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={card}
        ) 



