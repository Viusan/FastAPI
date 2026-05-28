from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#this line basically says if DATABASE_URL env variable exists inside docker, use postgresql
#if it does not exist then we use sqlitepy 
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

def create_engine_with_retry():
    retries = 5
    while retries > 0:
        try:
            engine = create_engine(SQLALCHEMY_DATABASE_URL)
            engine.connect()
            return engine
        except Exception:
            retries -= 1
            print(f"Database not ready, retrying... {retries} attempts left")
            time.sleep(3)
    raise Exception("Could not connect to database")


engine = create_engine(SQLALCHEMY_DATABASE_URL) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #a factory to create sessions

Base = declarative_base() #where db models will inherit from