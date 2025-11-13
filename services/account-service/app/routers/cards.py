from fastapi import APIRouter, Request 
from fastapi.responses import JSONResponse
from fastapi import status
from app.models.request_models import *
from app.models.response_models import *
from app.services.account_service import create_account_service, get_accounts_service, get_account_types
from app.services.card_service import get_cards_service
from app.utils.authentication import check_jwt_user_auth
from app.exceptions.authentication_exception import *
from app.exceptions.service_exception import *


router = APIRouter(prefix="/card")


@router.post("/create", response_model=AccountResponse)
def create_account(account_create_request:AccountCreateRequest, request:Request):
    
    return 1

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



