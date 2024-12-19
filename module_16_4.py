from fastapi import FastAPI, Path, HTTPException
from typing import Annotated, List
from pydantic import BaseModel


app = FastAPI()

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get('/users')
async def get_users() -> List[User]:
    return users

@app.post("/user/{user_name}/{age}", response_model=str)
async def create_user(user: User, user_name: Annotated[str, Path(min_length=4, max_length=20, description="Enter username", example="Igor")],
        age: int = Path(ge=18, le=120, description="Enter age", example=56)) -> str:
    new_id = (users[-1].id + 1) if users else 1
    new_user = User(id=new_id, username=user_name, age=age)
    users.append(new_user)
    return new_user
    return  f"User {new_id} is registered"


@app.put("/user/{user_id}/{user_name}/{age}")
async def update_user(user_name: Annotated[str, Path(min_length=4, max_length=20, description="Enter username", example="Igor")],
        age: int = Path(ge=18, le=120, description="Enter age", example=56),
        user_id: int = Path(ge=0)) -> str:
    for existing_user in users:
        if existing_user.id == user_id:
            existing_user.username = user_name
            existing_user.age = age
            return f"The user {user_id} is updated."
    raise HTTPException(status_code=404, detail="Пользователь не найден.")


@app.delete("/user/{user_id}", response_model=str)
async def delete_user(user_id: int = Path(ge=0)) -> str:
    for index, existing_user in enumerate(users):
        if existing_user.id == user_id:
            users.pop(index)
            return f"Пользователь с ID {user_id} удален."

    raise HTTPException(status_code=404, detail="Пользователь не найден.")