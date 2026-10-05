import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGHORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 1

def create_token(data:dict):
    payload = data.copy()

    payload.update({
        "exp": datetime.now(timezone.utc) + timedelta(TOKEN_EXPIRE_HOURS)
    })

    return jwt.encode(
            payload,
            SECRET_KEY,
            ALGHORITHM
        )    
