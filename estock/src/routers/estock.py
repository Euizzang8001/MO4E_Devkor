from fastapi import APIRouter, Depends

from schemas.estock import User, UserCreate, UserAll
from services.estock import UserService

router = APIRouter(
    prefix='/estock',
    tags=["estock"],
    responses={
        404: { "description": "Not found"}
    }
)

@router.get('/all', response_model=UserAll)
async def get_all_users(service: UserService = Depends()):
    result = service.get_all_users()
    return result

@router.get('/get', response_model=User)
async def get_user(user_id: str, service: UserService = Depends()):
    result = service.get_user_by_id(user_id)
    return result

@router.post('/create', response_model=User)
async def create_user(user_create_dto: UserCreate, service: UserService = Depends()):
    result = service.create_user(user_create_dto)
    return result