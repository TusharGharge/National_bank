from pydantic import BaseModel
from pydantic import BaseModel,EmailStr, conint
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name:str
    phone_number:str

class UserOut(BaseModel):
    email: EmailStr
    id:int
    name:str
    phone_number:str
    created_at:datetime
    class Config:
        orm_mode = True

class Deposite(BaseModel):
    # user_id:int
    # account_number:float
    amount:float

class UserLogin(BaseModel):
    email:EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None

class AccountOpen(BaseModel):
    pan_number:str

class Balance(BaseModel):
    balance:float
    accountholder_id:int

class Statement(BaseModel):
    balance: float
    amount:float
    # receiver_account:int
    id:int
    method:str
    status:str
    created_at:datetime
    class Config:
        orm_mode = True

class Transfer(BaseModel):
    amount:float
    account_number:int

class Login(BaseModel):
    email: EmailStr
    password: str

class Checkout(BaseModel):
    email: EmailStr
    id:int
    name:str
    phone_number:str
    created_at:datetime
    account_number:int
    
    class Config:
        orm_mode = True
    
class Verifymail(BaseModel):
    otp: str
    email: EmailStr



