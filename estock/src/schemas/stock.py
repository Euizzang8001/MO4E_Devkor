from pydantic import BaseModel
from typing import List, Optional

class StockBase(BaseModel):
    samsung: int
    samsung_lstm: int
    kakao: int
    kakao_lstm: int
    naver: int
    naver_lstm: int
    hive: int
    hive_lstm: int
    cj: int
    cj_lstm: int

class Stock(StockBase):
    date: str

    class Config:
        orm_mode = True

class StockRevise(StockBase):
    pass

class StockAll(StockBase):
    total: int
    users: Optional[List[Stock]]

class StockCreate(StockBase):
    pass
