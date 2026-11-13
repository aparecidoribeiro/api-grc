from pydantic import BaseModel
from typing import Literal
from datetime import date as type_date, time

class EventCreate(BaseModel):
    title: str
    description: str
    type: Literal["meeting", "event"]
    date: type_date
    start_time: time
    location: str

class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    type: Literal["meeting", "event"] | None = None
    date: type_date | None = None
    start_time: time | None = None
    location: str | None = None