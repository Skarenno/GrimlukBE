from sqlalchemy import Column, String, DateTime, ForeignKey, TIMESTAMP, BOOLEAN, Integer, func 
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserCredentialsModel(Base):
    __tablename__ = "user_credentials"

    username = Column(String(50), primary_key=True, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class UserModel(Base):
    __tablename__ = "user"

    id = Column(String, primary_key = True, unique=True, index=True, nullable=False)
    tax_code = Column(String(16), nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, unique=True,nullable=False)
    birth_date = Column(DateTime, nullable=False)
    mail = Column(String, nullable=False)
    username = Column(String, ForeignKey("user_credentials.username"), nullable=False)
    phone = Column(String, nullable=True)
    gender = Column(String(1), nullable=False)
    residence_address_1 = Column(String, nullable=False)
    residence_address_2 = Column(String, nullable=True)
    postal_code = Column(String(5), nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    province = Column(String(2), nullable=False)


class UserAccessLogModel(Base):
    __tablename__ = "access_log"

    id=Column(Integer, primary_key=True, index=True,nullable=False,autoincrement=True)
    username = Column(String, nullable=False)
    access_timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    ip_address = Column(String, nullable=False)
    successful = Column(BOOLEAN, nullable=False)