from datetime import date
from pydantic import BaseModel, Field
from typing import Literal

class UserCreate(BaseModel):
    name: str
    cpf: str
    birth_date: date
    phone: str
    email: str
    password: str

class UserResponse(BaseModel):
    name: str
    cpf: str
    birth_date: date
    phone: str
    email: str
    role: str
    family_id: str

class AdminCreate(BaseModel):
    name: str
    email: str
    password: str

class FamilyCreate(BaseModel):
    production_type: str

class UserWithFamilyCreate(BaseModel):
    user: UserCreate
    family: FamilyCreate

class LoginRequest(BaseModel):
    email: str
    password: str

class MemberCreate(BaseModel):
    name: str | None = None
    cpf: str | None = None
    birth_date: date | None
    relationship: str | None = None
    phone: str | None = None
    email: str | None = None

class InventoryCreate(BaseModel):
    name: str
    category: Literal["insumo", "ferramenta", "máquina"]
    quantity: float = Field(default=1, ge=1)
    unit: str = "unidade"
    description: str | None = None

class InventoryUpdate(BaseModel):
    name: str | None = None
    category: Literal["insumo", "ferramenta", "máquina"] | None = None
    quantity: float | None = Field(default=None, ge=1)
    unit: str | None = None
    description: str | None = None