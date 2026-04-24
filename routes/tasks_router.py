from fastapi import HTTPException, APIRouter
from models import Task

tasks : dict[int, Task] = {}
# tasks router
taskRouter = APIRouter(prefix="/tasks", tags=["tasks"])

@taskRouter.get("/", status_code=200)
def get_all_tasks() -> list[Task]:
    return list(tasks.values())

@taskRouter.get("/{id}", status_code=200)
def get_task(id: int) -> Task:
    task = tasks.get(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@taskRouter.post("/", status_code=201)
def create_task(task: Task) -> Task:
    tasks[task.id] = task
    return task

@taskRouter.put("/{id}", status_code=200)
def update_task(id: int, payload: Task) -> Task:
    if id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task with given Id {id} not found")
    updated = tasks[id].model_copy(
        update = payload.model_dump(exclude={"id","created_at"})
    )
    tasks[id] = updated
    return updated

#delete an item and return the deleted item
@taskRouter.delete("/{id}", status_code=200)
def delete_task(id: int) -> Task:
    if id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task with given Id {id} not found")

    task = tasks.pop(id)
    return task