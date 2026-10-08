from datetime import date
from pydantic import BaseModel

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
    name: str
    cpf: str
    birth_date: date
    relationship: str


