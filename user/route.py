from fastapi import APIRouter, HTTPException
from user.schema import UserInput, UserModel, PasswordInput

user_router = APIRouter()


@user_router.get("/users")
def get_users():
    return UserModel.find_all()


@user_router.post("/register", status_code=201)
def create_user(payload: UserInput):
    if UserModel.find_one(username=payload.username):
        raise HTTPException(status_code=400, detail="username already taken")
    user = UserModel.model_validate(payload.model_dump())
    user.save()
    return {"message": "created user", "data": user}


@user_router.put("/user/{user_id}")
def change_password(user_id: int, payload: PasswordInput):
    user = UserModel.find_one(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password = payload.password
    user.save()
    return {"message": f"changed passwrod for {user_id}"}


@user_router.delete("/user/{user_id}")
def delete_user(user_id: int):
    user = UserModel.find_one(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete()
    return {"message": f"deleted user with id {user_id}"}
