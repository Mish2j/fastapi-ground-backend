from pydantic import BaseModel
from typing import Optional


class Event(BaseModel):
    timestamp: str
    type: str
    status: str
    message: str
    command: str | None = None