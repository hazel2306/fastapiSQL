# from typing import Annotated

# from fastapi import Depends, FastAPI, HTTPException, Query
# from sqlmodel import Field, Session, SQLModel, create_engine, select


# class Hero(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     age: int | None = Field(default=None, index=True)
#     secret_name: str

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from dotenv import load_dotenv
import os

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_PATH')

# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DTB_USERNAME}:{settings.DTB_PWD}@{settings.DTB_HOSTNAME}/{settings.DTB_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# connect to dtb in PgAdmin
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### if using pure sql

# import psycopg
# import time

# while True:
#     try:
#         conn = psycopg.connect(
#             host='localhost', dbname='fastapi', user='postgres', password='aBr!ghtFutur3')
#         cursor = conn.cursor()
#         #need to store in variables to maintain the connection outside the loop
#         print("Database connection successful")
#         break 
#     except Exception as error:
#         print("Database connection error", error)
#         time.sleep(2)