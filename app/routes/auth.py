from fastapi import APIRouter

from app.schemas.user import UserWithFamilyCreate, UserResponse
from app.utils.security import hash_password

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)
@router.post(
    "/users",
    response_model=UserResponse)
async def create_user(data: UserWithFamilyCreate):

    hashed_password = hash_password(data.user.password)

    return {
        "name": data.user.name,
        "cpf": data.user.cpf,
        "email": data.user.email,
        "password": hashed_password,
        "production_type": data.production_type,
        "members_count": data.members_count
    }