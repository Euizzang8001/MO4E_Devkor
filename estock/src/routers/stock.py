from fastapi import APIRouter, Depends
from schemas.stock import Stock, StockAll, StockRevise, StockCreate
from services.stock import StockService

router = APIRouter(
    prefix='/estock',
    tags=["estock"],
    responses={
        404: { "description": "Not found"}
    }
)

#모든 주식 정보 get
@router.get('/all-stock', response_model=StockAll)
async def get_all_stock(service: StockService = Depends()):
    result = service.get_all_stock()
    return result

#해당 주식 정보 수정
@router.put('/revise-stock/{date}', response_model = Stock)
async def revivse_user(date: str, stock_revise_dto: Stock, service: StockService = Depends()):
    result = service.revise_stock(date, stock_revise_dto)
    return result

#오늘의 주식 정보 db 저장
@router.post('/create-stock', response_model=StockCreate)
async def create_stock(stock_create_dto: StockCreate, service: StockService = Depends()):
    result = service.create_stock(stock_create_dto)
    return result

#해당 주식 정보 get
@router.get('/get-stock', response_model=Stock)
async def get_stock(date: str, service: StockService = Depends()):
    result = service.get_stock_by_date(date)
    return result