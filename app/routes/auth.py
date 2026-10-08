from fastapi import APIRouter, HTTPException
from app.schemas.user import LoginRequest
from app.utils.security import verify_password
from app.database.conection import users_collection

from app.utils.jwt import create_token

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
    
    #Cria token de acesso
    token_data = {
        "sub": str(user["_id"]),
        "role": user["role"],
    }

    if user["role"] == "user":
        token_data.update({"family_id": str(user["family_id"])})

    acess_token = create_token(token_data)     

    return {
        "message": "Usuário logado com sucesso",
        "access_token": acess_token,
        "token_type": "bearer"
        }


