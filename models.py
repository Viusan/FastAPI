from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Task(Base):
    __tablename__ = "tasks" #tables name in db

    #primary key being true now auto increments id and creates unique
    #nullable being false means it cant be empty
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    done = Column(Boolean, default=False)