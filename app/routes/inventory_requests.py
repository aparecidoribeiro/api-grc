from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from datetime import datetime, timezone

from app.database.conection import inventory_collection, inventory_request_collection
from app.schemas.inventory_request import InventoryRequest

from app.dependencies import get_current_user, get_current_admin

router = APIRouter(
    prefix="/inventory_request",
    tags=["Inventory Request"],
)

@router.post(
    "/"
)
async def request_inventory(
    request: InventoryRequest,
    user: dict = Depends(get_current_user)
    ):

    item = await inventory_collection.find_one(
        {"_id": ObjectId(request.item_id)}
    )

    if not item:
        raise HTTPException(
            status_code=404, 
            detail="Erro item não encontrado no inventário"
        )

    if request.quantity > item["quantity"]:
        raise HTTPException(
            status_code=400,
            detail="Erro, quantidade solicitada maior que a disponível"
        )

    user_id = user["sub"]
    family_id = user["family_id"]

    if not user_id or not family_id:
        raise HTTPException(
            status_code=403,
            detail="Erro, não possui família vinculada"
        )

    #Criar solicitação
    request = {
        "item_id": ObjectId(request.item_id),
        "family_id": ObjectId(family_id),
        "requested_by": ObjectId(user_id),
        "quantity": request.quantity,
        "status": "pending",
        "created_at": datetime.now(timezone.utc),
        "expected_return_date": (
            request.expected_return_date.isoformat()
            if request.expected_return_date
            else None
        ),
        "picked_up_at": None,
        "returned_at": None
    }

    try:
        result = await inventory_request_collection.insert_one(request)

        return {
            "message": "Solicitação enviada com sucesso"
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao enviar a solicitação"
        )
