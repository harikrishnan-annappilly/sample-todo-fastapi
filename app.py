from fastapi import FastAPI
from user.route import user_router
from task.route import task_router

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(task_router, prefix="/task", tags=["Task"])
