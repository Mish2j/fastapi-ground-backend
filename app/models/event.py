from pydantic import BaseModel


class Event(BaseModel):
    timestamp: str
    type: str
    status: str
    message: str
    command: str | None = None
