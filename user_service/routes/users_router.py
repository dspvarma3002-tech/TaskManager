from fastapi import APIRouter, HTTPException
from user_service.config import TASK_SERVICE_URL
from user_service.models import User
import httpx

users : dict[int, User] = {}
userRouter = APIRouter(prefix="/users", tags=["users"])

#returns all the users
@userRouter.get("/", status_code=200)
def get_all_users():
    return list(users.values())

#returns a single user by userId
@userRouter.get("/{id}", status_code=200)
def get_user(id: int) -> User:
    user = users.get(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Creates a single user record
@userRouter.post("/", status_code=201)
def create_user(user : User):
    users[user.id] = user
    return user

@userRouter.put("/{id}", status_code=200)
def update_user(id: int, payload: User):
    if id not in users:
        raise HTTPException(status_code=404, detail=f"User with given Id {id} not found")

    users[id] = users[id].model_copy(
        update = payload.model_dump(exclude = {"id","created_at"})
    )
    return users[id]

@userRouter.delete("/{id}", status_code=200)
def delete_user(id: int):
    if id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        resposne = httpx.put(f"{TASK_SERVICE_URL}/tasks/unassign-user/{id}")
    except httpx.HTTPError:
        raise HTTPException(status_code=503, detail="Task service unavailable")
    user = users.pop(id)
    return user
