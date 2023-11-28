import datetime
from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    user_name: str
    age: int
    priority: str
    score: int
    prediction: int
    delta: int

    
class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: str
    last_revised_time: datetime.datetime
    
    class Config:
        orm_mode = True

class UserAll(BaseModel):
    total: int
    users: Optional[List[User]]

class UserRevise(UserBase):
    pass

class UserRank(BaseModel):
    users: Optional[List[User]]

    