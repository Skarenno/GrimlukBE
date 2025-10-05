from sqlalchemy.orm import Session
from app.models.mappers import map_user_info_to_db
from app.models.request_models import *
from app.models.db_models import *
from app.utils.authentication import hash_password, verify_password, generate_jwt
from app.exceptions.service_exceptions import *


def register_user_service(request:UserRegisterRequest, db: Session):
    # Check if username exists
    existing = db.query(UserCredentialsModel).filter_by(username=request.username).first()
    if existing:
        raise UserAlreadyExistsError

    # Create new user
    new_user = UserCredentialsModel(
        username=request.username,
        password=hash_password(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return generate_jwt(new_user.username)


def login_user_service(request:UserLoginRequest, db:Session):
    db_user = db.query(UserCredentialsModel).filter(UserCredentialsModel.username == request.username).first()

    if(not db_user or not verify_password(request.password, db_user.password)):
            raise UserDoesNotExistError
    
    return generate_jwt(db_user.username)

def update_user_info_service(request:UserInfoRequest, db:Session):
    db_user = db.query(UserModel).filter(UserModel.username == request.username).first()
    db_user = map_user_info_to_db(request, existing_user=db_user)

    if db_user not in db:
        db.add(db_user)

    db.commit()
    db.refresh(db_user)
    return db_user


def check_user_existance(username: str, db:Session):
    db_user = db.query(UserCredentialsModel).filter(UserCredentialsModel.username == username).first()
    if not db_user:
        raise UserDoesNotExistError
    
    
    return db.query(UserModel).filter(UserModel.username == username).first()
    
