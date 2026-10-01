from fastapi import APIRouter, HTTPException
from app.schemas.user import LoginRequest
from app.utils.security import verify_password
from app.database.conection import users_collection


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post(
    "/login"
)
async def login(data: LoginRequest):

    user = await users_collection.find_one({
        "email": data.email
    })

    if not user:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos"
        )
    
    #Compara as senhas
    password_is_correct = verify_password(
        data.password,
        user["password"]
    )

    if not password_is_correct:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos"
        )

    return {"message": "Usuário logado com sucesso"}


