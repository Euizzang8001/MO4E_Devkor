from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
import uuid
from fastapi import HTTPException

from config.database import get_db
from models.user import User as UserModel
from schemas.user import User, UserCreate, UserRevise

class UserRepository():
    def __init__(self, db: Session = Depends(get_db)) -> None : 
        self.db = db
    
    def get_all_users(self) -> List[User]:
        return self.db.query(UserModel).all()
    
    def get_count_by_user(self) -> int:
        return self.db.query(UserModel).count()
    
    def get_user_by_id(self, user_id: str) -> User:
        return self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
    
    def get_user_by_name(self, user_name: str) -> User:
        return self.db.query(UserModel).filter(UserModel.user_name == user_name).first()
    
    def delete_user(self, user_id: str) -> User:
        exist = self.get_user_by_id(user_id = user_id)
        if not exist:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            self.db.delete(exist)
            self.db.commit()
            return exist

    def revise_user(self, user_id: str, user_revise_dto: UserRevise, commit:bool = True) -> User:
        exist =self.get_user_by_id(user_id = user_id)
        if not exist:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            self.db.delete(exist)
            data = UserModel(
                user_id = user_id,
                user_name = user_revise_dto.user_name,
                age = user_revise_dto.age,
                priority = user_revise_dto.priority,
                score=user_revise_dto.score,
                delta = user_revise_dto.delta,
                prediction = user_revise_dto.prediction,
            )
            self.db.add(data)
            if commit:
                self.db.commit()
                self.db.refresh(data)
            return data
            

    def create_user(self, user_create_dto: UserCreate, commit: bool = True) -> User:
        user_name = user_create_dto.user_name
        age = user_create_dto.age
        priority = user_create_dto.priority
        score = user_create_dto.score
        prediction = user_create_dto.prediction
        delta = user_create_dto.delta
        exists = self.get_user_by_name(user_name=user_name)
        if exists:
            return exists
        else:
            user_id = str(uuid.uuid4())[:6]
            data = UserModel(
                user_id=user_id,
                user_name=user_name,
                age=age,
                priority=priority,
                score = score,
                prediction=prediction,
                delta=delta,
            )
            self.db.add(data)
            if commit:
                self.db.commit()
                self.db.refresh(data)
            return data
    
    def get_rank(self) -> List[User]:
        return self.db.query(UserModel).order_by(UserModel.score.desc()).limit(10).all()
        
       