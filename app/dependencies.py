from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import verify_token

oauth = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

#Verica se o token é valido
async def get_current_user(token: str = Depends(oauth)):
    payload = verify_token(token)

    return payload

#Verifica se o token é valido e se o usuário é admin
async def get_current_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem acessar esta rota"
        )

    return current_user
