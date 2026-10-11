from fastapi import APIRouter, HTTPException, Depends
from app.dependencies import get_current_admin, get_current_user
from app.schemas.user import MemberCreate as Member
from app.database.conection import families_collection
from bson import ObjectId

router = APIRouter(
    prefix="/families",
    tags=["Families"],
    dependencies=[Depends(get_current_user)]
)

#Cria membro da familia
@router.post(
    "/{family_id}/members", 
    dependencies=[Depends(get_current_admin)]
    )
async def create_member(family_id: str, data: Member):
    family = await families_collection.find_one({
        "_id": ObjectId(family_id)
    })

    if not family:
        raise HTTPException(
            status_code=404,
            detail="Família não encontrada"
        )

    verify_cpf = await families_collection.find_one({
        "_id": ObjectId(family_id),
        "members.cpf": data.cpf
    })

    if verify_cpf:
        raise HTTPException(
            status_code=409,
            detail="CPF já cadastrado nesta família"
        )

    try:
        await families_collection.update_one(
            {"_id": ObjectId(family_id)},
            {
                "$push": {
                    "members": {
                        "_id": ObjectId(),
                        "name": data.name,
                        "cpf": data.cpf,
                        "birth_date": data.birth_date.isoformat(),
                        "relationship": data.relationship
                    }
                },
                "$inc": {
                    "members_count": 1
                }
            }
        )
        
        return {
            "message": "Membro adicionado com sucesso"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Erro ao adicionar membro"
        )


#Pegas todas as familias
@router.get(
    "/",
    dependencies=[Depends(get_current_admin)]
    )
async def get_families():

    try:
        families = await families_collection.find().to_list(length=None)

        if not families:
            raise HTTPException(
                status_code=404,
                detail="Nenhuma família encontrada"
            )

        for family in families:
            family["_id"] = str(family["_id"])
            for member in family["members"]:
                member["_id"] = str(member["_id"])

        return families

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Erro ao buscar familias"
        )

#Pega uma família
@router.get("/{family_id}")
async def get_family(family_id: str):
    try:
        family = await families_collection.find_one({
            "_id": ObjectId(family_id)
            })

        family["_id"] = str(family["_id"])

        for member in family["members"]:
            member["_id"] = str(member["_id"])

        if not family:
            raise HTTPException(
                status_code=404,
                detail="Família não encontrada"
            )

        return family

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Erro ao buscar família"
        )