from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.dependencies import get_current_admin
from app.database.conection import events_collection, attendance_collection, users_collection

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)

@router.get(
    "/{event_id}",
    dependencies=[Depends(get_current_admin)]
)
async def get_attendance(event_id: str):
    result_event = await events_collection.find_one({"_id": ObjectId(event_id)})

    if not result_event:
        raise HTTPException(
            status_code=404,
            detail="Esse evento não existe"
            )

    if result_event["type"] == "event":
        raise HTTPException(
            status_code=400,
            detail="Esse tipo de evento não precisa de lista de presença"
        )

    result_attendance = await attendance_collection.find_one({"event_id": ObjectId(event_id)})

    try:
        #Se a lista de presença ainda não estive criada
        if not result_attendance:
            families = []

            list_user = await users_collection.find({"role": "user"}).to_list(length=None)

            for user in list_user:
                data_user = {
                    "family_id": str(user["_id"]),
                    "admin_family": str(user["family_id"]),
                    "admin_name": user["name"],
                    "present": False
                }

                families.append(data_user)

            await attendance_collection.insert_one(
                {
                    "event_id": ObjectId(event_id),
                    "families": families
                }
            )            

            return families
        
        else:
            result = await attendance_collection.find_one({"event_id": ObjectId(event_id)})

            result["_id"] = str(result["_id"])
            result["event_id"] = str(result["event_id"])

            for family in result["families"]:
                family["family_id"] = str(family["family_id"])
                family["admin_family"] = str(family["admin_family"])

            return result

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Erro ao criar lista de presença"
        )