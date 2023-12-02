from fastapi import Depends

from schemas.stock import Stock, StockAll, StockCreate, StockRevise
from repository.stock import StockRepository

class StockService():
    def __init__(self, repository: StockRepository = Depends()) -> None:
        self.repository = repository
    
    def get_all_stock(self) -> StockAll:
        stocks = self.repository.get_all_stock()
        total = self.repository.get_count_by_stock()
        return {
            "total": total,
            "stocks": stocks,
        } 
    
    def get_stock_by_date(self, date: str) -> Stock:
        return self.repository.get_stock_by_date(date)
    
    def create_stock(self, stock_create_dto: StockCreate) -> Stock:
        return self.repository.create_stock(stock_create_dto)
    
    def revise_stock(self, date:str, stock_revise_dto: StockRevise) -> Stock:
        return self.repository.revise_stock(date, stock_revise_dto)