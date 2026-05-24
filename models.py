from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

class Task(Base):
    __tablename__ = "tasks" #tables name in db

    #primary key being true now auto increments id and creates unique
    #nullable being false means it cant be empty
    id = Column(Integer, primary_key=True, index=True) 
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False) #user.id refferes to id collumn in user table, thats how it links to the table
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    done = Column(Boolean, default=False)