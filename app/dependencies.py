from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import verify_token

oauth = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

async def get_current_user(token: str = Depends(oauth)):
    payload = verify_token(token)

    return payload