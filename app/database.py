from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import psycopg2


# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

SQLALCHEMY_DATABASE_URL = f'postgresql://yourbankuser:ZoDUVYGZjR2mroCALa0Qf4kAxtpp6TNI@dpg-cob7gc21hbls73anrrqg-a.oregon-postgres.render.com:5432/yourbank_lt8j'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
