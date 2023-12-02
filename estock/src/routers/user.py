from fastapi import APIRouter, Depends
from schemas.user import User, UserCreate, UserAll, UserRevise, UserRank
from services.user import UserService

router = APIRouter(
    prefix='/estock',
    tags=["estock"],
    responses={
        404: { "description": "Not found"}
    }
)

#모든 사용자 정보 get
@router.get('/all', response_model=UserAll)
async def get_all_users(service: UserService = Depends()):
    result = service.get_all_users()
    return result

#10위권의 사용자 data get
@router.get('/rank', response_model=UserRank)
async def get_rank(service: UserService = Depends()):
    result = service.get_rank()
    return result

#id로 사용자 정보 get
@router.get('/get', response_model=User)
async def get_user(user_id: str, service: UserService = Depends()):
    result = service.get_user_by_id(user_id)
    return result

#new 사용자 생성
@router.post('/create', response_model=UserCreate)
async def create_user(user_create_dto: UserCreate, service: UserService = Depends()):
    result = service.create_user(user_create_dto)
    return result

#사용자 정보 수정
@router.put('/revise/{user_id}', response_model = User)
async def revivse_user(user_id: str, user_revise_dto: UserRevise, service: UserService = Depends()):
    result = service.revise_user(user_id, user_revise_dto)
    return result

#사용자 삭제
@router.delete('/delete/{user_id}',response_model = User)
async def delete_user(user_id: str, service: UserService = Depends()):
    result = service.delete_user(user_id)
    return result

