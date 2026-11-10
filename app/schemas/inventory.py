from pydantic import BaseModel, Field
from datetime import date
from typing import Literal

class InventoryRequest(BaseModel):
    item_id: str
    name: str
    category: str
    quantity: int = Field(ge=1)
    expected_return_date: date | None = None

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