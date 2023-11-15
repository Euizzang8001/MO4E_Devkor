from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

with open("data.json", "r") as file:
    data_content = file.read()

db = json.loads(data_content)

class User(BaseModel):
    id: int
    name: str
    age: int
    role: str

@app.get("/users")
async def all_users():
    return db

@app.get("/users/{user_id}")
async def read_users(user_id: str):
    user = db.get(user_id)
    if user is None:
        raise HTTPException(status_code = 404, detail = "User not Found")
    return user

@app.put("/users/{user_id}")
async def update_users(user_id: str, user: User):
    if user_id not in db:
        raise HTTPException(status_code = 404, detail = "User not Found")
    db[user_id].update(user.dict())
    return {"user_id":user_id, "user_info":db[user_id]}

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    if user_id not in db:
        raise HTTPException(status_code = 404, detail = "User not Found")
    db_delete = db.pop(user_id)
    return {"message": f"{user_id} 유저가 깔끔히 영원히 평생 제거되었습니다!ㅋ"}