from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user, get_current_admin
from bson import ObjectId

from app.database.conection import notifications_collection

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get(
    "/"
)
async def get_notifications(
    user: dict = Depends(get_current_user)
):

    user_id = ObjectId(user["sub"])

    try:

        result = await notifications_collection.find(
            {"user_id": user_id}
            ).sort("created_at", -1).to_list(length=None)

        for notification in result:
            notification["_id"] = str(notification["_id"])
            notification["user_id"] = str(notification["user_id"])
            notification["request_id"] = str(notification["request_id"])
            notification["created_at"] = notification["created_at"].strftime("%d/%m/%Y")

        return result

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao buscar notificações"
        )