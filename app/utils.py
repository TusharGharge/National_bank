from passlib.context import CryptContext
import smtplib
import random
from random import randrange
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
import re

def haseddata(password):
    return pwd_context.hash(password)

def verify(plan_password, hashed_password):
    return pwd_context.verify(plan_password,hashed_password)

def Commit(db,data):
    db.add(data)
    db.commit()
    db.refresh(data)

def Mailgenrator(emailaddress):
    email='tushargharge05@gmail.com'
    reciver_email=emailaddress
    otp=str(randrange(1000,9999))
    subject='Sign up for YourBank - Email Verification'
    message=f"""
    Dear User,


    Thank you for registering with our service. To complete your registration, Your One time password as below

    {otp}

    If you did not request this verification, please disregard this email.


    Thank you,
    YourBank

    """
    text=f"Subject: {subject}\n\n{message}"
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(email,"etae xrkb xfva goxd")
    server.sendmail(email,reciver_email,text)
    return otp

def isValidPanCardNo(panCardNo):
 
    # Regex to check valid
    # PAN Card number
    regex = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
 
    # Compile the ReGex
    p = re.compile(regex)
 
    # If the PAN Card number
    # is empty return false
    if(panCardNo == None):
        return False
 
    # Return if the PAN Card number
    # matched the ReGex
    if(re.search(p, panCardNo) and
       len(panCardNo) == 10):
        return True
    else:
        return False