from pydantic import BaseModel, Field
from datetime import date


class InventoryRequest(BaseModel):
    item_id: str
    name: str
    category: str
    quantity: int = Field(ge=1)
    expected_return_date: date | None = None