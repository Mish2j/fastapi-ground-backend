from datetime import datetime

from pydantic import BaseModel

from app.constants import Command, SafeModeReason
from app.core.events.event_types import EventStatus, EventType


class Event(BaseModel):
    timestamp: datetime
    type: EventType
    status: EventStatus
    message: str
    command: Command | None = None
    reason: SafeModeReason | None = None
