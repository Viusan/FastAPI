from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Task(BaseModel): #no need for id here since it auto increments and creates unique
    name: str
    description: str
    done: bool = False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

tasks = []

@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)): #everytime this is called, fastAPI runs get_db(), it gets db sessiona nd passes it in as db
    return db.query(models.Task).all() #this just fetches everything in db

@app.get("/tasks/{task_id}")
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first() #we ask db to find row where id matches, and first returns first match or none if nothing is found
    if task is None:
        raise HTTPException(status_code=404, detail = "Task not found")   
    return task

@app.post("/tasks")
def create_task(task: Task, db: Session = Depends(get_db)): 
    #we create SQLAlchemy model obj from pydantic data that comes in
    #pydantic one receives the data from API and SQLAlchemy one goes into the db
    db_task = models.Task(name=task.name, description=task.description, done=task.done) 
    db.add(db_task)
    db.commit()
    db.refresh(db_task)#refreshes the obj in db so it auto increments id that SQLite assinged it
    return db_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task, db: Session = Depends(get_db)):
    #we are just filtering to find the right row with id
    #and then we are assigning the right info and updating the database
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail = "Task not found")   
    db_task.name = task.name
    db_task.description = task.description
    db_task.done = task.done
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Successfully removed"}