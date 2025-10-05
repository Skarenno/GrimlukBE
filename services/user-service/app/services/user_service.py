from sqlalchemy.orm import Session
from app.models.mappers import map_user_info_to_db
from app.models.request_models import *
from app.models.db_models import *
from app.utils.authentication import hash_password, verify_password, generate_jwt
from app.exceptions.service_exceptions import *
from datetime import datetime

def register_user_service(request:UserRegisterRequest, db: Session):
    existing = db.query(UserCredentialsModel).filter_by(username=request.username).first()
    if existing:
        raise UserAlreadyExistsError

    new_user = UserCredentialsModel(
        username=request.username,
        password=hash_password(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return generate_jwt(new_user.username)


def login_user_service(request:UserLoginRequest, ip_address:str, db:Session):
    db_user = db.query(UserCredentialsModel).filter(UserCredentialsModel.username == request.username).first()

    if(not db_user):
            raise UserDoesNotExistError
    if(not verify_password(request.password, db_user.password)):
            insert_access_log(request, ip_address, db, successful=False)
            raise PasswordInvalidError

    insert_access_log(request,ip_address, db)
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
    
def insert_access_log(request:UserLoginRequest, ip_address:str, db:Session, successful=True):
     log_insert = UserAccessLogModel(
          username = request.username,
          ip_address = ip_address,
          successful = successful,
          access_timestamp = datetime.now()
     )

     db.add(log_insert)
     db.commit()

     return