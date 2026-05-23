from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    id: int
    name: str
    description: str
    done: bool = False

tasks = []

@app.get("/tasks")
def read_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    for t in tasks:
        if t.id == task_id:
            return t #returning the match we found
    raise HTTPException(status_code=404, detail="Task not found")    

@app.post("/tasks")
def create_task(task: Task): #says expect a task to come in, and match Task class i defined
    task.id = len(tasks) + 1 #see array size and increment by 1 so new tasks get a unique id
    #here the whole object is being sent in to us, so we can just append it to our tasks directly
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    for t in tasks:
        if t.id == task_id:
            #since we are saying a task object matching our task class is coming, we can update it all
            t.name = task.name
            t.description = task.description
            t.done = task.done
            return t
    raise HTTPException(status_code=404, detail="Task not found") #we using 404 since that is not found 

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for t in tasks:
        if t.id == task_id:
            tasks.remove(t)
            return {"message": "Successfully removed"}
    raise HTTPException(status_code=404, detail="Task not found")