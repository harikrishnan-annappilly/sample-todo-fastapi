from fastapi import FastAPI
from user.route import user_router

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["User"])
