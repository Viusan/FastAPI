from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#this line basically says if DATABASE_URL env variable exists inside docker, use postgresql
#if it does not exist then we use sqlitepy 
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

#function tries to connect to database, if it fails it tries again up to 5 times
#reason being in compsoe file we have depends on db, which waits for postgresql container to start
#not for postgresql to actually be ready to accept connections (which takes a couple extra seconds)
def create_engine_with_retry():
    retries = 10
    while retries > 0:
        try:
            engine = create_engine(SQLALCHEMY_DATABASE_URL)
            engine.connect()
            return engine
        except Exception:
            retries -= 1
            print(f"Database not ready, retrying... {retries} attempts left")
            time.sleep(5)
    raise Exception("Could not connect to database")


engine = create_engine(SQLALCHEMY_DATABASE_URL) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #a factory to create sessions

Base = declarative_base() #where db models will inherit from