from fastapi import FastAPI
from fastapi import Body, FastAPI, Response,status,HTTPException,Depends,APIRouter
from ..database import engine,SessionLocal,get_db
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..routers import user
from random import randrange
from typing import List
from . import oauth

router=APIRouter(
    prefix='/bank',
    tags=['Bank_feature']
)


# account=[{
#     'account_number':67475578885,
#     'balance':10000.0,
#     'user_id':1,
# }]

# def findpost(user_id):
#     for p in account:
#         if p["user_id"]==user_id:
#             return p
# @router.get("/")
# def root():
#     return {"message": "Hello World"}


@router.post("/createaccount",status_code=status.HTTP_200_OK)
def createaccount(accountdetails:schemas.AccountOpen,current_user:int=Depends(oauth.get_current_user),db: Session = Depends(get_db)):
    bankaccount=db.query(models.Account).filter(models.Account.pan_number==accountdetails.pan_number).first()
    if bankaccount:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Pan number is already exists, Already account has been created")
    useraccount=db.query(models.Account).filter(models.Account.accountholder_id==current_user).first()
    if useraccount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Account already exists")
    print("current_user",current_user)
    account_number_data=randrange(1,1000000)
    amount=0.0

    new_account=models.Account(amount=amount,account_number=account_number_data,accountholder_id=current_user,**accountdetails.dict())
    # new_account=models.Account(accountholder_id=current_user)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    method="Created Account"
    status="Successfull"
    transactrion=models.Transaction(method=method,amount=amount,balance=amount,status=status,accountholder_id=current_user)
    db.add(transactrion)
    db.commit()
    db.refresh(transactrion)

    return {"message":"account has been created"}



@router.get("/balance",response_model=schemas.Balance)
def get_balanced(current_user:int=Depends(oauth.get_current_user),db: Session = Depends(get_db)):
    # data=account[0]["balance"]
    data=db.query(models.Transaction).filter(models.Transaction.accountholder_id==current_user).order_by(models.Transaction.created_at.desc()).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid user ID")
    return data


@router.put("/deposite")
def deposite_money(update_balance:schemas.Deposite,current_user:int=Depends(oauth.get_current_user),db: Session = Depends(get_db)):
    status=" "
    data=db.query(models.Transaction).filter(models.Transaction.accountholder_id==current_user).order_by(models.Transaction.created_at.desc()).first()
 
    print("data.amount",data.balance)
    cal=update_balance.amount < 499
    if cal:
        status="failed"
        transactrion=models.Transaction(amount=update_balance.amount,balance=data.balance,method="Deposite",status=status,accountholder_id=current_user)
        db.add(transactrion)
        db.commit()
        db.refresh(transactrion)
        return {"message":"Deposite amount should be min 500"}
  
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid user ID")
    else:
         status="successful"
    totalbalance=data.balance
    totaldata=totalbalance+update_balance.amount
    print(totaldata)
    transactrion=models.Transaction(amount=update_balance.amount,balance=totaldata,method="Deposite",status=status,accountholder_id=current_user)
    db.add(transactrion)
    db.commit()
    db.refresh(transactrion)

    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user_id not found {update_balance.user_id}")
    # # data=(user["balance"])+update_balance.amount
    return {"data":"Deposite successful"}

@router.put("/widthdraw")
def widthdraw_money(update_balance:schemas.Deposite,current_user:int=Depends(oauth.get_current_user),db: Session = Depends(get_db)):
    status=" "
    data=db.query(models.Transaction).filter(models.Transaction.accountholder_id==current_user).order_by(models.Transaction.created_at.desc()).first()
    #Checking account balace before withdraw money, if widthfraw amount is > the error
    if update_balance.amount > data.balance:
        status="failed"
        transactrion=models.Transaction(amount=update_balance.amount,balance=data.balance,method="Withdraw",status=status,accountholder_id=current_user)
        db.add(transactrion)
        db.commit()
        db.refresh(transactrion)
        return {"message":"insufficient fund"}

        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid user ID")
    else:
         status="successful"
    # logic for substraction of ammount from balance
    totalbalance=data.balance
    totaldata=totalbalance-update_balance.amount
    transactrion=models.Transaction(amount=update_balance.amount,balance=totaldata,method="Withdraw",status=status,accountholder_id=current_user)
    db.add(transactrion)
    db.commit()
    db.refresh(transactrion)

    return {"message":"Widthdraw Sucessful"}

@router.get("/Statement",response_model=List[schemas.Statement])
def statement(current_user:int=Depends(oauth.get_current_user),db: Session = Depends(get_db)):
    data=db.query(models.Transaction).filter(models.Transaction.accountholder_id==current_user).all()
    return data


@router.put("/transfer")
def statement(tansfer_amount:schemas.Transfer,current_user:int=Depends(oauth.get_current_user),db: Session = Depends(get_db)):
    # amount account number as input 
    # testcases
    # 1) entered account is present in user (sendders account)
    # 2) check entered account present or not
    # 3) if both works
    # 4) send money from sender account (deduct amount)
    # 5) transfer money to receiver account (addition of amount)
    status=" "
    transaction_id=randrange(1,1000000)
    receiver_account=db.query(models.Account).filter(models.Account.account_number==tansfer_amount.account_number).first()
    if not receiver_account:
        return {"message":"Receiver account not found"}
    data=db.query(models.Transaction).filter(models.Transaction.accountholder_id==current_user).order_by(models.Transaction.created_at.desc()).first()
    if tansfer_amount.amount > data.balance:
        # raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail=f"insufficient fund") 
    
        status="failed"
        transactrion=models.Transaction(amount=tansfer_amount.amount,balance=data.balance,method="Tansfer",status=status,accountholder_id=current_user)
        db.add(transactrion)
        db.commit()
        db.refresh(transactrion)
        return {"message":"insufficient fund"}
    
    #transfer money logic 
    #decution of money from user(send account)
    totalbalance=data.balance
    totaldata=totalbalance-tansfer_amount.amount
    print(totaldata)
    transactrion=models.Transaction(transaction_id=transaction_id,status="successful",amount=tansfer_amount.amount,balance=totaldata,method="Transfred",accountholder_id=current_user)
    db.add(transactrion)
    db.commit()
    db.refresh(transactrion)
    
    #transfer of money to receiver account
    receiver_account_data=db.query(models.Transaction).filter(models.Transaction.accountholder_id==receiver_account.accountholder_id).order_by(models.Transaction.created_at.desc()).first()
    totalbalance_of_reciver=receiver_account_data.balance
    totaldata_of_reciver=totalbalance_of_reciver+tansfer_amount.amount
    print(totaldata_of_reciver)
    transactrion_data=models.Transaction(transaction_id=transaction_id,amount=tansfer_amount.amount,balance=totaldata_of_reciver,method="Received",status="successful",accountholder_id=receiver_account.accountholder_id,receiver_account=current_user)
    db.add(transactrion_data)
    db.commit()
    db.refresh(transactrion_data)





    
    return {"message":"Amount has been transfered successfully"}