from sqlalchemy import (
    Column, Integer, String, Numeric, Boolean, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, nullable = False)
    user_id = Column(Integer, index=True, nullable=False)
    account_number = Column(String(34), unique=True, nullable=False)
    account_type = Column(String(20), nullable=False)
    currency = Column(String(3), default="EUR")
    balance = Column(Numeric(15, 2), default=0.00)
    available_balance = Column(Numeric(15, 2), default=0.00)
    credit_limit = Column(Numeric(15, 2), default=0.00)
    interest_rate = Column(Numeric(5, 2), default=0.00)
    opened_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(String(20), default="active")
    is_joint = Column(Boolean, default=False)
    branch_code = Column(String(10), nullable=True)
    product_code = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    cards = relationship("Card", back_populates="account", cascade="all, delete-orphan")

    transactions = relationship("Transaction", back_populates="account")


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)

    card_number = Column(String(16), nullable=False )
    last4 = Column(String(4), nullable=False)
    cardholder_name = Column(String(100), nullable=False)
    expiry_month = Column(Integer, nullable=False)
    expiry_year = Column(Integer, nullable=False)
    card_type = Column(String(20), nullable=False)
    network = Column(String(20))
    issuer = Column(String(50))
    daily_limit = Column(Numeric(15, 2))
    online_payments_enabled = Column(Boolean, default=True)
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), server_default=func.now())
    last_used_at = Column(DateTime(timezone=True), nullable=True)

    # Relationship
    account = relationship("Account", back_populates="cards")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    type = Column(String(20), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(String)
    target_account = Column(String(20))

    account = relationship("Account", back_populates="transactions")

    
class AccountType(Base):
    __tablename__ = "account_types"

    code = Column(String(5), primary_key=True)
    name = Column(String(50))


class BranchCode(Base):
    __tablename__ = "branch_codes"

    code = Column(String(5), primary_key=True)
    name = Column(String(50))
