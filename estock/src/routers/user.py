from fastapi import APIRouter, Depends

from schemas.user import User, UserCreate, UserAll, UserRevise
from services.user import UserService

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

@router.put('/revise/{user_id}', response_model = User)
async def revivse_user(user_id: str, user_revise_dto: UserRevise, service: UserService = Depends()):
    result = service.revise_user(user_id, user_revise_dto)
    return result

# @router.delete('/delete/{user_id}',response_model = User)
# async def delete_user(user_id: str, service: UserService = Depends()):
#     result = service.delete_user(user_id)
#     return result

@router.get('/{user_id}/priority', response_model = User)
async def priority_result(user_id: str, service: UserService = Depends()):
    result = service.get_priority_result(user_id)
    return result

    