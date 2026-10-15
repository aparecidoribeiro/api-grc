from fastapi import APIRouter, HTTPException, Depends
from app.dependencies import get_current_admin, get_current_user
from app.schemas.user import MemberCreate as Member
from app.database.conection import families_collection, users_collection
from bson import ObjectId

from app.database.conection import client

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


#Pega todas as familias
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

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao buscar família"
        )


#Atualizar membro
@router.put(
    "/{family_id}/members/{member_id}",
    dependencies=[Depends(get_current_admin)]
    )
async def update_member(family_id: str, member_id: str, data: Member):
    try:
        family = await families_collection.find_one({
            "_id": ObjectId(family_id),
            "members._id": ObjectId(member_id)
            })
        
        if not family:
            raise HTTPException(
                status_code=404,
                detail="Família ou membro não encontrado"
            )
        # Verifica se o user é o responsável
        def verify_relationship(family: dict, member_id: str):
            for member in family["members"]:
                if str(member["_id"]) == member_id:
                    return member["relationship"] == "admin"
            
            return False
            
        #Se não for o admin da família
        if not verify_relationship(family, member_id):
            update = await families_collection.update_one(
                {"_id": ObjectId(family_id),
                "members._id": ObjectId(member_id)},
                {
                    "$set": {
                        "members.$.name": data.name,
                        "members.$.cpf": data.cpf,
                        "members.$.birth_date": data.birth_date.isoformat(),
                        "members.$.relationship": data.relationship,
                    }
                }    
            )

            return {
                "message": "Membro atualizado com sucesso"
            }
       
        #Se for o admin da família
        else:

            async with client.start_session() as session:
                async with await session.start_transaction():

                    await families_collection.update_one(
                        {"_id": ObjectId(family_id),
                        "members._id": ObjectId(member_id)},
                        {
                            "$set": {
                                "members.$.name": data.name,
                                "members.$.cpf": data.cpf,
                                "members.$.birth_date": data.birth_date.isoformat()
                            }
                        },
                        session=session
                    )

                    await users_collection.update_one(
                        {
                            "_id": ObjectId(member_id)
                        },
                        {
                            "$set": {
                                "name": data.name,
                                "cpf": data.cpf,
                                "birth_date": data.birth_date.isoformat(),
                                "phone": data.phone,
                                "email": data.email
                            }
                        },
                        session=session
                    )

            return {
                "message": "Membro atualizado com sucesso"
                }


    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao editar membro"
        )


@router.delete(
    "/{family_id}/members/{member_id}"
)
async def delete_member(
    family_id: str,
    member_id: str,
    dependencies=[Depends(get_current_admin)]
    ):
    
    try:
        family = await families_collection.find_one(
            {
                "_id": ObjectId(family_id),
                "members._id": ObjectId(member_id)
            }
        )

        if not family:
            raise HTTPException(
                status_code=404, 
                detail="Família ou membro não encontrado"
            )

        def verify_admin():
            for member in family["members"]: 
                if str(member["_id"]) == member_id and member["relationship"] == "admin":
                    return True
            
            return False

        if verify_admin():
            raise HTTPException(
                status_code=403,
                detail="Não é permitido deletar o responsável da família"
            )

        await families_collection.update_one(
            {
                "_id": ObjectId(family_id)
            }, 
            {
                "$pull": {
                    "members": {
                        "_id": ObjectId(member_id)
                        }
                    },
                "$inc": {
                    "members_count": -1
                }
            }
            )
        return {
            "message": "Membro deletado com sucesso"
        }

    except HTTPException: 
        raise

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Erro ao deletar membro"
        )
