from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
import uuid
from fastapi import HTTPException
from datetime import date
from config.database import get_db
from models.stock import Stock as StockModel
from schemas.stock import Stock, StockCreate, StockRevise


# class UserService():
#     def __init__(self, repository: StockRepository = Depends()) -> None:
#         self.repository = repository
    
#     def get_all_stock(self) -> StockAll:
#         stocks = self.repository.get_all_stock()
#         total = self.repository.get_count_by_stock()
#         return {
#             "total": total,
#             "stocks": stocks,
#         } 
    
#     def get_stock(self, date: str) -> Stock:
#         return self.repository.get_stock_by_date(date)
    
#     def create_stock(self, stock_create_dto: StockCreate) -> Stock:
#         return self.repository.create_stock(stock_create_dto)
    
#     def revivse_stock(self, date:str, stock_revise_dto: StockRevise) -> Stock:
#         return self.repository.revise_stock(date, stock_revise_dto)

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
