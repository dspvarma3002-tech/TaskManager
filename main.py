from fastapi import FastAPI,APIRouter
from models import Task
from routes import tasks_router

app = FastAPI()

# task router
app.include_router(tasks_router.taskRouter)

@app.get("/")
def root():
    return {"message": "Task Manager"}
