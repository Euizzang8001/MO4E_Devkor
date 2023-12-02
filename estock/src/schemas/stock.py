from datetime import date
from pydantic import BaseModel
from typing import List, Optional

class StockBase(BaseModel):
    samsung_price: int
    samsung_pred: int
    kakao_price: int
    kakao_pred: int
    naver_price: int
    naver_pred: int
    hive_price: int
    hive_pred: int
    cj_price: int
    cj_pred: int

class Stock(StockBase):
    Date: date.today()

    class Config:
        orm_mode = True

class StockRevise(StockBase):
    pass

class StockAll(StockBase):
    total: int
    users: Optional[List[Stock]]

class StockCreate(StockBase):
    pass
