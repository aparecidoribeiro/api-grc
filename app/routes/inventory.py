from fastapi import APIRouter, HTTPException, Depends
from app.dependencies import get_current_user, get_current_admin

from app.database.conection import inventory_collection
from app.schemas.user import InventoryCreate

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"], 
    dependencies=[Depends(get_current_user)]
)

@router.post(
    "/",
    dependencies=[Depends(get_current_admin)]
)
async def create_inventory(data: InventoryCreate):
    try:

        dict_data = data.model_dump()

        inventory = await inventory_collection.find_one(
            {"name": data.name}
        )

        if inventory:
            raise HTTPException(
                status_code=409,
                detail="Erro já possui um item com esse nome"
            )

        await inventory_collection.insert_one(dict_data)

        return {
            "message": "Item criado com sucesso"
        }

    except Exception:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Erro ao adicionar item ao inventário"
        )


@router.get(
    "/"
)
async def get_inventory():

    try:
        inventory = await inventory_collection.find().to_list(length=None)
        if not inventory:
            raise HTTPException(
                status_code=200,
                detail="Não possui nenhum item no inventário"
            )

        for item in inventory:
            item["_id"] = str(item["_id"])

        return inventory
    
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao buscar itens do inventário"
        )