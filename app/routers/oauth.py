from jose import JWTError, jwt
from .. import schemas
from datetime import datetime, timedelta, timezone
from fastapi import Body, FastAPI, Response,status,HTTPException,Depends,APIRouter
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
from ..config import settings
import smtplib
import random
from random import randrange

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data:dict):
    to_encode=data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        token_data:str=payload.get("User_id")
        if id is None:
            raise credentials_exception
        # token_data=schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"could not validate credentials",headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token,credentials_exception)

