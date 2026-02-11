import jwt
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, HTTPException
from user.schema import UserInput, UserModel

auth_router = APIRouter()
SECRET_KEY = "secret-key"
ALGORITHM = "HS256"


@auth_router.post("/login")
def login_page(payload: UserInput):
    user = UserModel.find_one(username=payload.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password != payload.password:
        raise HTTPException(status_code=400, detail="Incorrect password")

    refresh_data = {
        "sub": payload.username,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
    }
    access_data = {
        **refresh_data,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
        "type": "access",
    }
    refresh_token = jwt.encode(refresh_data, SECRET_KEY, ALGORITHM)
    access_token = jwt.encode(access_data, SECRET_KEY, ALGORITHM)
    return {"access_token": access_token, "refresh_token": refresh_token}
