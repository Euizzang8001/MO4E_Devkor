from fastapi import Depends

from schemas.user import User, UserAll, UserCreate, UserRevise, UserRank, Stock, StockRevise, StockAll, StockCreate
from repository.user import UserRepository, StockRepository

class UserService():
    def __init__(self, repository: UserRepository = Depends()) -> None:
        self.repository = repository
    
    def get_all_users(self) -> UserAll:
        users = self.repository.get_all_users()
        total = self.repository.get_count_by_user()
        return {
            "total": total,
            "users": users,
        } 
    
    def get_user_by_id(self, user_id: str) -> User:
        return self.repository.get_user_by_id(user_id)
    
    def create_user(self, user_create_dto: UserCreate) -> User:
        return self.repository.create_user(user_create_dto)
    
    def revise_user(self, user_id:str, user_revise_dto: UserRevise) -> User:
        return self.repository.revise_user(user_id, user_revise_dto)
    
    def delete_user(self, user_id:str) -> User:
        return self.repository.delete_user(user_id)
    
    def get_rank(self) -> UserRank:
        users = self.repository.get_rank()
        return {"users": users,}

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