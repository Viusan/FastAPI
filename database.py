from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./task.db" #this tells where db files live and "./" creates a task.db in project folder

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) #engine that connect to db, dont need to worry about the code as much here

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #a factory to create sessions

Base = declarative_base() #where db models will inherit from