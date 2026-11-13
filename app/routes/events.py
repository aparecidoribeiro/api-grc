from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_admin
from app.schemas.events import EventCreate, EventUpdate
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

@router.patch(
    "/{event_id}",
    dependencies=[Depends(get_current_admin)]
)
async def update_event(data: EventUpdate, event_id: str):

    data = data.model_dump(exclude_unset=True)

    if "date" in data and data["date"] is not None:
        data["date"] = data["date"].isoformat()
    
    if "start_time" in data and data["start_time"] is not None:
        data["start_time"] = data["start_time"].isoformat()

    data["updated_at"] = data_now

    if not data: 
        raise HTTPException(
            status_code=400,
            detail="Nenhum campo foi enviado para atualizar"
        )

    try:
        result = await events_collection.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": data}
            )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Evento não encontrado"
            )

        return {
            "message": "Evento atualizado com sucesso"
        }

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Erro ao editar evento"
        )
