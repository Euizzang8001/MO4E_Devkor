from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
import uuid
from fastapi import HTTPException

from config.database import get_db
from models.user import User as UserModel
from models.user import Stock as StockModel
from schemas.user import User, UserCreate, UserRevise, Stock, StockCreate, StockRevise
from datetime import date

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
    
class StockRepository():
    def __init__(self, db: Session = Depends(get_db)) -> None : 
        self.db = db
    
    def get_all_stock(self) -> List[Stock]:
        return self.db.query(StockModel).all()
    
    def get_count_by_stock(self) -> int:
        return self.db.query(StockModel).count()
    
    def get_stock_by_date(self, date: str) -> Stock:
        return self.db.query(StockModel).filter(StockModel.date == date).first()

    def revise_stock(self, date: str, stock_revise_dto: StockRevise, commit:bool = True) -> Stock:
        exist =self.get_stock_by_date(date = date)
        if not exist:
            raise HTTPException(status_code=404, detail="Stock not found")
        else:
            self.db.delete(exist)
            data = StockModel(
                date = date,
                samsung = stock_revise_dto.samsung,
                kakao = stock_revise_dto.kakao,
                naver = stock_revise_dto.naver,
                hive = stock_revise_dto.hive,
                cj = stock_revise_dto.cj,
                samsung_lstm = stock_revise_dto.samsung_lstm,
                kakao_lstm = stock_revise_dto.kakao_lstm,
                naver_lstm = stock_revise_dto.naver_lstm,
                hive_lstm = stock_revise_dto.hive_lstm,
                cj_lstm = stock_revise_dto.cj_lstm,
            )
            self.db.add(data)
            if commit:
                self.db.commit()
                self.db.refresh(data)
            return data
            

    def create_stock(self, stock_create_dto: StockCreate, commit: bool = True) -> Stock:
        samsung = stock_create_dto.samsung
        kakao = stock_create_dto.kakao
        naver = stock_create_dto.naver
        hive = stock_create_dto.hive
        cj = stock_create_dto.cj
        samsung_lstm = stock_create_dto.samsung_lstm
        kakao_lstm = stock_create_dto.kakao_lstm
        naver_lstm = stock_create_dto.naver_lstm
        hive_lstm = stock_create_dto.hive_lstm
        cj_lstm = stock_create_dto.cj_lstm
        today_date = date.today()
        exists = self.get_stock_by_date(date=today_date)
        if exists:
            return exists
        else:
            data = StockModel(
                date = today_date,
                samsung = samsung,
                kakao = kakao,
                naver = naver,
                hive = hive,
                cj = cj,
                samsung_lstm = samsung_lstm,
                kakao_lstm = kakao_lstm,
                naver_lstm = naver_lstm,
                hive_lstm = hive_lstm,
                cj_lstm = cj_lstm,
            )
            self.db.add(data)
            if commit:
                self.db.commit()
                self.db.refresh(data)
            return data
        
       