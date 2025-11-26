from sqlalchemy import (
    Column, Integer, String, Numeric, Boolean, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    s_account_id = Column(Integer)
    r_account_id = Column(Integer)
    s_account_number = Column(String)
    r_account_number = Column(String)
    user_id =Column(Integer)
    amount = Column(Numeric(15, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String)
    description = Column(String)
    reject_reason = Column(String)
    is_external =Column(Boolean)
    is_blocking_account = Column(Boolean)

    