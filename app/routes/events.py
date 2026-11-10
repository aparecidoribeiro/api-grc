from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_admin
from app.schemas.events import EventCreate
from app.database.conection import events_collection
from datetime import datetime, timezone
from bson import ObjectId

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

data_now = datetime.now(timezone.utc)

@router.post(
    "/",
    dependencies=[Depends(get_current_admin)]
)
async def create_event(data: EventCreate):
    event = {
    "title": data.title,
    "description": data.description,
    "type": data.type,
    "date": data.date.isoformat(),
    "start_time": data.start_time.isoformat(),
    "location": data.location,
    "created_at": data_now,
    "updated_at": data_now
    }

    try:

        await events_collection.insert_one(event)

        return {
            "message": "Evento criado com sucesso"
        }

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Erro ao criar evento"
        )

@router.get(
    "/",
    dependencies=[Depends(get_current_admin)]
)
async def get_events():
    try:

        result = await events_collection.find().to_list(length=None)

        for event in result:
            event["_id"] = str(event["_id"])

        return result

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao buscar eventos"
        )

