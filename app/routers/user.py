from fastapi import Body, FastAPI, Response,status,HTTPException,Depends,APIRouter
from .. import schemas
from .. import models,utils
from ..database import engine,SessionLocal,get_db

from sqlalchemy.orm import Session

router=APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    hased_password=utils.haseddata(user.password)
    user.password=hased_password
    new_user=models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id : {id} does not exists")
    return user