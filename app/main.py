from fastapi import FastAPI
from fastapi import Body, FastAPI, Response,status,HTTPException,Depends,APIRouter
from .database import engine,SessionLocal,get_db
from . import models,schemas
from sqlalchemy.orm import Session
from .routers import user,bank_features,auth
from passlib.context import CryptContext

from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI()

app.include_router(user.router)
app.include_router(bank_features.router)
app.include_router(auth.router)
