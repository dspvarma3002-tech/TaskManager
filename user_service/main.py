from fastapi import FastAPI
from user_service.routes import users_router

app = FastAPI()

# user router
app.include_router(users_router.userRouter)

@app.get("/")
def root():
    return {"message": "USER_SERVICE"}