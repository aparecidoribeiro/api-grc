from fastapi import APIRouter

from app.database.conection import client


router = APIRouter()
@router.get("/test")
async def test():

    try:
        await client.admin.command("ping")
        return { "message": "Banco conectado!" }

    except Exception:
        return {"Error"}
