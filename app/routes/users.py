from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.utils.security import hash_password
from app.database.conection import users_collection, families_collection
from app.schemas.user import UserWithFamilyCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


#Cria usuário
@router.post(
    "/",
    status_code=201
    )
async def create_user(data: UserWithFamilyCreate):

    try:

        family = {
            "production_type": data.family.production_type,
            "members_count": data.family.members_count,
            "members": []
        }

        family_result = await families_collection.insert_one(family)

        #ID fa família criada
        family_id = family_result.inserted_id

        hashed_password = hash_password(data.user.password)

        user = {
            "name": data.user.name,
            "cpf": data.user.cpf,
            "birth_date": data.user.birth_date.isoformat(),
            "phone": data.user.phone,
            "email": data.user.email,
            "password": hashed_password,
            "role": "user",
            "family_id": family_id,
        }

        user_result = await users_collection.insert_one(user)

        return {
            "message": "Usuário Criado com sucesso"
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail= "Erro ao criar o usuário"
        )
