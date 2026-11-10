from pydantic import BaseModel
from typing import Literal
from datetime import date, time

class EventCreate(BaseModel):
    title: str
    description: str
    type: Literal["meeting", "event"]
    date: date
    start_time: time
    location: str