import datetime
from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    user_name: str
    age: int
    priority: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: str
    created_datetime: datetime.datetime
    
    class Config:
        orm_mode = True

class UserAll(BaseModel):
    total: int
    users: Optional[List[User]]

class UserRevise(UserBase):
    pass
    