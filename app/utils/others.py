from datetime import datetime, timezone
from app.database.conection import notifications_collection

async def create_notification(
    user_id,
    request_id,
    title,
    message
):
    notification = {
        "user_id": user_id,
        "request_id": request_id,
        "title": title,
        "message": message,
        "read": False,
        "created_at": datetime.now(timezone.utc)
    }

    await notifications_collection.insert_one(notification)