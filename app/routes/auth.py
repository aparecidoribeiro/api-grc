from fastapi import APIRouter, HTTPException, Response, Depends
from app.schemas.user import LoginRequest
from app.utils.security import verify_password
from app.database.conection import users_collection

from app.utils.jwt import create_token

from bson import ObjectId

from app.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post(
    "/login"
)
async def login(data: LoginRequest, response: Response):

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

    user_data = {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "family_id": str(user.get("family_id"))
    }   

    response.set_cookie(
        key="token",
        value=acess_token,
        httponly=True,
        secure=False,
        samesite="lax"
    )


    return {
        "message": "Usuário logado com sucesso",
        "user": user_data
        }


@router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):

    user_data = await users_collection.find_one({
        "_id": ObjectId(user["sub"])
    })

    if not user_data:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return {
        "user": {
            "id": str(user_data["_id"]),
            "name": user_data["name"],
            "email": user_data["email"],
            "role": user_data["role"],
            "family_id": str(user_data.get("family_id"))
        }
    }