from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.utils.security import hash_password
from app.schemas.user import UserWithFamilyCreate, UserResponse, AdminCreate
from app.database.conection import client
from fastapi import Depends
from app.dependencies import get_current_user
# Minhas coleções | MongoDB
from app.database.conection import users_collection, families_collection

router = APIRouter(
    prefix="/users",
    tags=["Users"], 
)

#Cria usuário | role = user
@router.post(
    "/",
    status_code=201
    ) 
async def create_user(data: UserWithFamilyCreate):

    verify_user = await users_collection.find_one({
        "$or": [
            {"email": data.user.email },
            {"cpf": data.user.cpf},
        ]
    })

    if verify_user:
        raise HTTPException(
            status_code=409,
            detail= "E-mail ou CPF já cadastrado"
        )

    try:
        async with client.start_session() as session:
            async with await session.start_transaction():
                family = {
                    "production_type": data.family.production_type,
                    "members_count": data.family.members_count,
                    "members": []
                }

                family_result = await families_collection.insert_one(family, session=session)

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

                user_result = await users_collection.insert_one(user, session=session)

                return {
                    "message": "Usuário Criado com sucesso"
                }
    except Exception as e:
        print("Erro:", e)
        raise HTTPException(
            status_code=500,
            detail= "Erro ao criar o usuário"
            )

#Cria usuário | role = admin
@router.post(
    "/admin",
    status_code=201
)
async def create_admin(data: AdminCreate):
    verify_user = await users_collection.find_one({
        "email": data.email
    })

    if verify_user:
        raise HTTPException(
            status_code=409,
            detail="Error: Já existe um usuário com esse email"
        )

    try:
        hashed_password = hash_password(data.password)

        admin = {
            "name": data.name,
            "email": data.email,
            "password": hashed_password,
            "role": "admin"
        }

        admin_result = await users_collection.insert_one(admin)

        return {
            "message": "Usuário criado com sucesso"
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao criar usuário"
        )


@router.post(
    "/family"
)
async def create_family(current_user: dict = Depends(get_current_user)):
    return current_user