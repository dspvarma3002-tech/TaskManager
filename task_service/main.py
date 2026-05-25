from fastapi import FastAPI
from task_service.routes import tasks_router

app = FastAPI()

# task router
app.include_router(tasks_router.taskRouter)

@app.get("/")
def root():
    return {"message": "Task Manager"}
