from fastapi import BackgroundTasks, FastAPI
from fastapi import Body, FastAPI, Response,status,HTTPException,Depends,APIRouter
from ..database import engine,SessionLocal,get_db
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..routers import user
from random import randrange
from typing import List
from . import oauth
from sqlalchemy import func
from fastapi.middleware.cors import CORSMiddleware
from collections import ChainMap
from sqlalchemy import create_engine, func, extract,case
from sqlalchemy.orm import sessionmaker # Import your Transaction model here
from sqlalchemy.orm import aliased
from datetime import datetime
from datetime import datetime
from celery.schedules import crontab
import redis
import json
from ..celery_worker import redis_client,celery


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


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
@router.get("/")
def demo():
    return {"message":"fectch data successfully"}

@router.post("/createaccount",status_code=status.HTTP_200_OK)
def createaccount(accountdetails:schemas.AccountOpen,current_user:int=Depends(oauth.get_current_user),db: Session = Depends(get_db)):
    bankaccount=db.query(models.Account).filter(models.Account.pan_number==accountdetails.pan_number).first()
    data=utils.isValidPanCardNo(accountdetails.pan_number)
    if data == False:
        return {"message": "Invalid Pancard Number"}
    if bankaccount:
        return {"message":"Pan number is already exists"}
    useraccount=db.query(models.Account).filter(models.Account.accountholder_id==current_user).first()
    if useraccount:
        raise {"message":"Account already exists"}
    print("current_user",current_user)
    account_number_data=randrange(1,1000000)
    amount=0.0

    new_account=models.Account(amount=amount,account_number=account_number_data,accountholder_id=current_user,**accountdetails.dict())
    # new_account=models.Account(accountholder_id=current_user)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    method="Created Account"
    status="successful"
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
 
    cal=update_balance.amount < 499
    if cal:
        status="failed"
        transactrion=models.Transaction(amount=update_balance.amount,balance=data.balance,method="Deposit",status=status,accountholder_id=current_user)
        db.add(transactrion)
        db.commit()
        db.refresh(transactrion)
        return {"message":"Deposit amount should be min 500"}
  
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid user ID")
    else:
         status="successful"
    totalbalance=data.balance
    totaldata=totalbalance+update_balance.amount
    print(totaldata)
    transactrion=models.Transaction(amount=update_balance.amount,balance=totaldata,method="Deposit",status=status,accountholder_id=current_user)
    db.add(transactrion)
    db.commit()
    db.refresh(transactrion)

    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user_id not found {update_balance.user_id}")
    # # data=(user["balance"])+update_balance.amount
    return {"message":"Deposit successful"}

@router.put("/widthdraw")
def widthdraw_money(update_balance:schemas.Deposite,current_user:int=Depends(oauth.get_current_user),db: Session = Depends(get_db)):
    if update_balance.amount < 1:
        return {"message": "Please enter valid amount"}

    status=" "
    data=db.query(models.Transaction).filter(models.Transaction.accountholder_id==current_user).order_by(models.Transaction.created_at.desc()).first()
    #Checking account balace before withdraw money, if widthfraw amount is > the error
    if update_balance.amount > data.balance:
        status="failed"
        transactrion=models.Transaction(amount=update_balance.amount,balance=data.balance,method="Withdraw",status=status,accountholder_id=current_user)
        db.add(transactrion)
        db.commit()
        db.refresh(transactrion)
        return {"message":"Insufficient fund"}

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
def transfer(tansfer_amount:schemas.Transfer,current_user:int=Depends(oauth.get_current_user),db: Session = Depends(get_db)):
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
        transactrion=models.Transaction(amount=tansfer_amount.amount,balance=data.balance,method="Transferred",status=status,accountholder_id=current_user)
        db.add(transactrion)
        db.commit()
        db.refresh(transactrion)
        return {"message":"Insufficient fund"}
    
    #transfer money logic 
    #decution of money from user(send account)
    totalbalance=data.balance
    totaldata=totalbalance-tansfer_amount.amount
    print(totaldata)
    transactrion=models.Transaction(transaction_id=transaction_id,status="successful",amount=tansfer_amount.amount,balance=totaldata,method="Transferred",accountholder_id=current_user)
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

@router.get("/checkaccount")
def checkaccount(current_user:int=Depends(oauth.get_current_user),db: Session = Depends(get_db)):
    data=db.query(models.Account).filter(models.Account.accountholder_id==current_user).first()
    if not data:
        return {"messge":"Please create account"}
    result=db.query(models.Account,models.Users).join(models.Users,models.Users.id==models.Account.accountholder_id,isouter=True).filter(models.Users.id==current_user).first()

    print(result.Account)

    return {result.Account,result.Users}




@router.get("/transactionamountmonthly")
def get_transactions_monthly(db: Session = Depends(get_db)):
    current_datetime = datetime.now()

    # Extract the month and year from the current date
    current_month = current_datetime.month
    current_year = current_datetime.year

    # print("Current month:", current_month)
    # print("Current year:", current_year)
    # data=db.query(models.TrasactionData).filter(models.TrasactionData.transaction_month==current_month,models.TrasactionData.transaction_year==current_year)
    # if data:
    #     return {"messge":"Automation is already runnned"}
    # Write the SQLAlchemy query
    query = db.query(
        models.Transaction.accountholder_id,
        extract('month', models.Transaction.created_at).label('transaction_month'),
        extract('year', models.Transaction.created_at).label('transaction_year'),
        func.count().label('total_transactions'),
        func.sum(case((models.Transaction.method == 'Deposit', models.Transaction.amount), else_=0)).label('total_deposit'),
        func.sum(case((models.Transaction.method == 'Withdraw', models.Transaction.amount), else_=0)).label('total_withdraw'),
        func.sum(case((models.Transaction.method == 'Transferred', models.Transaction.amount), else_=0)).label('total_transferred'),
        func.sum(case((models.Transaction.method == 'Received', models.Transaction.amount), else_=0)).label('total_received'),
        func.coalesce(func.avg(models.Transaction.balance), 0).label('mab')
    ).filter(
        extract('month', models.Transaction.created_at) == 4,
        extract('year', models.Transaction.created_at) == 2024
    ).group_by(
        models.Transaction.accountholder_id,
        extract('month', models.Transaction.created_at),
        extract('year', models.Transaction.created_at)
    )

    # Execute the query and fetch the results
    results = query.all()

    # Convert results to JSON format
    transactions_json = []
    for row in results:
        transaction = {
            'accountholder_id': row[0],
            'transaction_month': row[1],
            'transaction_year': row[2],
            'total_transactions': row[3],
            'total_deposit': row[4],
            'total_withdraw': row[5],
            'total_transferred': row[6],
            'total_received': row[7],
            'mab': row[8]
        }
        transactionsall=models.TrasactionData(accountholder_id=row[0],transaction_month=row[1],transaction_year=row[2],total_transactions=row[3],total_deposit=row[4],total_withdraw=row[5],total_transferred=row[6],total_received=row[7],mab=row[8])
        print(transactionsall)          
        db.add(transactionsall)
        db.commit()
        # db.refresh(transactionsall)
        transactions_json.append(transaction)
        # transactionsall=models.TrasactionData(accountholder_id=row[0],transaction_month=row[1],transaction_year=row[2],total_transactions=row[3],total_deposit=row[4],total_withdraw=row[5],total_transferred=row[6],total_received=row[7],mab=row[8])
        # db.add(transactionsall)
        # db.commit()
        # db.refresh(transactionsall)
    return transactions_json


@celery.task
def get_transactions_daily(db: Session = Depends(get_db)):
    current_datetime = datetime.now()

    # Extract the year, month, and day from the current date
    current_year = current_datetime.year
    current_month = current_datetime.month
    current_day = current_datetime.day

    print("Current year:", current_year)
    print("Current month:", current_month)
    print("Current day:", current_day)
    
    # data = db.query(models.TrasactionDataDaily).filter(
    #     models.TrasactionDataDaily.day_transaction_year == current_year,
    #     models.TrasactionDataDaily.day_transaction_month == current_month,
    #     models.TrasactionDataDaily.day_transaction_day == current_day
    # ).first()

    # if data:
    #     return {"message": "Automation has already run for today"}
    

    # Write the SQLAlchemy query
    query = db.query(
        models.Transaction.accountholder_id,
        extract('day', models.Transaction.created_at).label('transaction_day'),
        func.count().label('total_transactions'),
        func.sum(case((models.Transaction.method == 'Deposit', models.Transaction.amount), else_=0)).label('total_deposit'),
        func.sum(case((models.Transaction.method == 'Withdraw', models.Transaction.amount), else_=0)).label('total_withdraw'),
        func.sum(case((models.Transaction.method == 'Transferred', models.Transaction.amount), else_=0)).label('total_transferred'),
        func.sum(case((models.Transaction.method == 'Received', models.Transaction.amount), else_=0)).label('total_received'),
        func.coalesce(func.avg(models.Transaction.balance), 0).label('mab')
    ).filter(
        extract('year', models.Transaction.created_at) == current_year,
        extract('month', models.Transaction.created_at) == current_month,
        extract('day', models.Transaction.created_at) == current_day
    ).group_by(
        models.Transaction.accountholder_id,
        extract('day', models.Transaction.created_at)
    )

    # Execute the query and fetch the results
    results = query.all()

    # Convert results to JSON format
    transactions_json = []
    for row in results:
        transaction = {
            'accountholder_id': row[0],
            'transaction_day': row[1],
            'total_transactions': row[2],
            'total_deposit': row[3],
            'total_withdraw': row[4],
            'total_transferred': row[5],
            'total_received': row[6],
            'mab': row[7]
        }
        transactionsall = models.TrasactionDataDaily(
            accountholder_id=row[0],
            day_transaction_year=current_year,
            day_transaction_month=current_month,
            day_transaction_day=current_day,
            day_total_transactions=row[2],
            day_total_deposit=row[3],
            day_total_withdraw=row[4],
            day_total_transferred=row[5],
            day_total_received=row[6],
            day_mab=row[7]
        )
        db.add(transactionsall)
        db.commit()
        transactions_json.append(transaction)

    return transactions_json


@router.get("/schedule_monthly_statements")
async def schedule_monthly_statements(background_tasks: BackgroundTasks):
    # Check if monthly statements are already scheduled
    # if redis_client.exists("monthly_statements_scheduled"):
    #     raise HTTPException(status_code=400, detail="Monthly statements are already scheduled")

    # Schedule monthly statements to run on the 1st of every month
    celery.conf.beat_schedule = {
        "generate-monthly-statements": {
            "task": "get_transactions_daily",
            "schedule": crontab(hour=22, minute=16)
            # "schedule": crontab(day_of_month=1, hour=0, minute=0),  # Run on the 1st of every month
        }
    }
    celery.conf.timezone = 'Asia/Kolkata'

    # Set flag to indicate monthly statements are scheduled
    redis_client.set("monthly_statements_scheduled", "true")
    print(redis_client.client_id)
    return {"message": "Monthly statements scheduled successfully"}

# def call_api():
#     # Replace 'your_api_endpoint' with the actual API endpoint you want to call
#     response = requests.get('http://127.0.0.1:8000/bank/transactionamountdaily')
#     # Process the response if needed
#     print("API called at", datetime.now())

# # Schedule the API call to occur every day at a specific time (e.g., 9:00 AM)
# schedule.every().day.at("18:07").do(call_api)

# # You can add more scheduled tasks here if needed

# while True:
#     schedule.run_pending()
#     time.sleep(1)


@celery.task
def add(x, y):
    return x + y