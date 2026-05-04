from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None = None
    friend_ids: list[int] | None = None
    password: str


@app.post("/user")
async def read_user(user: User) -> User:
    return user


class SafeUser(BaseModel):
    id: int
    name: str = "John Doe"
    friend_ids: list[int] | None = None


@app.post("/safe_user")
async def read_user(user: User) -> SafeUser:
    return user
