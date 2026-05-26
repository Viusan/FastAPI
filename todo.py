from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import hash_password, verify_password, create_access_token, verify_token
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

class User(BaseModel): #no need for id here since it auto increments and creates unique
    name: str
    email: str
    password: str

class Task(BaseModel): 
    name: str
    description: str
    done: bool = False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

#End Points for tasks
@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)): #everytime this is called, fastAPI runs get_db(), it gets db sessiona nd passes it in as db
    return db.query(models.Task).filter(models.Task.user_id == current_user.id).all() #this just fetches everything in db

@app.get("/tasks/{task_id}")
def read_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == current_user.id).first() 
    #we ask db to find row where id matches, and first returns first match or none if nothing is found
    #also saying find query where conditions must be true, so we are looking for where task id and user is is whatevery current_user.id is
    if task is None:
        raise HTTPException(status_code=404, detail = "Task not found")   
    return task

@app.post("/tasks")
def create_task(task: Task, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)): 
    #we create SQLAlchemy model obj from pydantic data that comes in
    #pydantic one receives the data from API and SQLAlchemy one goes into the db
    db_task = models.Task(user_id=current_user.id, name=task.name, description=task.description, done=task.done) 
    db.add(db_task)
    db.commit()
    db.refresh(db_task)#refreshes the obj in db so it auto increments id that SQLite assinged it
    return db_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    #we are just filtering to find the right row with id
    #and then we are assigning the right info and updating the database
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == current_user.id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail = "Task not found")   
    db_task.name = task.name
    db_task.description = task.description
    db_task.done = task.done
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == current_user.id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Successfully removed"}

#End Points for users
@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get("/user/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first() #we ask db to find row where id matches, and first returns first match or none if nothing is found
    if user is None:
        raise HTTPException(status_code=404, detail = "User not found")   
    return user

@app.post("/user")
def create_user(user: User, db: Session = Depends(get_db)):
    hashed = hash_password(user.password)
    db_user = models.User(name = user.name, email = user.email, password = hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#End Points for login
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #normally fastAPI built in form expects username and pass fieds, but we are using form_data.username for the email
    #since that is how /docs auth button works, so we just tricking it into thinking email is username
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}