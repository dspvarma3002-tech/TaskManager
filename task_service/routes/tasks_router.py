from fastapi import HTTPException, APIRouter
from task_service.models import Task
from task_service.config import USER_SERVICE_URL
import httpx

tasks : dict[int, Task] = {}
# tasks router
taskRouter = APIRouter(prefix="/tasks", tags=["tasks"])

@taskRouter.get("/", status_code=200)
def get_all_tasks() -> list[Task]:
    return list(tasks.values())

@taskRouter.get("/assigned/{user_id}", status_code=200)
def get_all_tasks_assigned_to_user(user_id : int) -> list[Task]:
    call_user_service(user_id)
    return [task for task in tasks.values() if task.assigned_to == user_id]

# un-assign the tasks related to a user
@taskRouter.put("/unassign-user/{user_id}", status_code=200)
def unassign_task(user_id: int):
    user_tasks = get_all_tasks_assigned_to_user(user_id)
    for task in user_tasks:
        tasks[task.id].assigned_to = None

@taskRouter.get("/{id}", status_code=200)
def get_task(id: int) -> Task:
    task = tasks.get(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@taskRouter.post("/", status_code=201)
def create_task(task: Task) -> Task:
    if task.assigned_to is not None:
        # call the user service to verify the user id
        call_user_service(task.assigned_to)
    tasks[task.id] = task
    return task

@taskRouter.put("/{id}", status_code=200)
def update_task(id: int, payload: Task) -> Task:
    if id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task with given Id {id} not found")
    if ((payload.assigned_to is not None)
            and
        (payload.assigned_to != tasks[id].assigned_to)):
        # call the user service to verify the user id
        call_user_service(payload.assigned_to)
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


def call_user_service(user_id: int):
    try:
        response = httpx.get(f"{USER_SERVICE_URL}/users/{user_id}")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="User service unavailable")
    if response.status_code == 404:
        raise HTTPException(status_code=400, detail=f"User {user_id} not found")