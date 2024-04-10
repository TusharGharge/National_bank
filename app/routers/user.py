from fastapi import Body, FastAPI, Response,status,HTTPException,Depends,APIRouter
from .. import schemas
from .. import models,utils
from ..database import engine,SessionLocal,get_db
from ..utils import Mailgenrator

from sqlalchemy.orm import Session

router=APIRouter(
    prefix='/user',
    tags=['Users']
)
system_otp=0

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    userdata=db.query(models.Users).filter(models.Users.email==user.email).first()
    if userdata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User already has account")
    userdata=db.query(models.Users).filter(models.Users.phone_number==user.phone_number).first()
    if userdata:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User already has account")
    hased_password=utils.haseddata(user.password)
    user.password=hased_password
    system_otp=Mailgenrator(user.email)
    # print(user)
    new_user=models.Users(**user.dict(),otp=system_otp)
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    system_otp=Mailgenrator(user.email)
    print("system_otp",system_otp)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id : {id} does not exists")
    return user

@router.post("/verifymail")
def verifymail(user: schemas.Verifymail,db: Session = Depends(get_db)):
    userdata=db.query(models.Users).filter(models.Users.email==user.email).first()
    if userdata:
        if userdata.otp==user.otp:
            return {"message":"user has been verified"}
        else:
            return {"message":"In valid otp"}
    else:
        return {"message":"Invalid user"}
    
