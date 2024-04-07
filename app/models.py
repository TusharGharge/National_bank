from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey,Integer, String,text,Float
from .database import Base
from sqlalchemy.orm import relationship

class Transaction(Base):
    __tablename__="Transaction"
    id=Column(Integer,primary_key=True,nullable=False)
    status=Column(String,nullable=False)
    method=Column(String,nullable=False)
    balance=Column(Float,nullable=False)
    amount=Column(Float,nullable=False)
    transaction_id=Column(Integer,nullable=True)
    receiver_account=Column(Integer,nullable=True)
    accountholder_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    owner=relationship("Users")



class Account(Base):
    __tablename__="account"
    id=Column(Integer,primary_key=True,nullable=False)
    account_number=Column(Integer,unique=True,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    pan_number=Column(String,nullable=False,unique=True)
    amount=Column(Float,nullable=False)
    accountholder_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    owner=relationship("Users")

class Users(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    phone_number=Column(String,nullable=False,unique=True)
    otp=Column(String,nullable=False,unique=True)

class TrasactionData(Base):
    __tablename__="TrasactionDataMonthly"
    id=Column(Integer,primary_key=True,nullable=False)
    transaction_month=Column(String,nullable=False)
    transaction_year=Column(String,nullable=False)
    total_transactions=Column(String,nullable=False)
    total_deposit=Column(String,nullable=False)
    total_withdraw=Column(String,nullable=False)
    total_transferred=Column(String,nullable=False)
    total_received=Column(String,nullable=False)
    mab=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    accountholder_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    owner=relationship("Users")



class TrasactionDataDaily(Base):
    __tablename__="TrasactionDataDaily"
    id=Column(Integer,primary_key=True,nullable=False)
    day_transaction_month=Column(String,nullable=False)
    day_transaction_year=Column(String,nullable=False)
    day_total_transactions=Column(String,nullable=False)
    day_total_deposit=Column(String,nullable=False)
    day_total_withdraw=Column(String,nullable=False)
    day_total_transferred=Column(String,nullable=False)
    day_total_received=Column(String,nullable=False)
    day_transaction_day=Column(String,nullable=False)
    day_mab=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    accountholder_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    owner=relationship("Users")
