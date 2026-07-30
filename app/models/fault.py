from datetime import datetime

from pydantic import BaseModel


class Fault(BaseModel):
    id: str
    type: str
    severity: str
    message: str
    created_at: datetime
    active: bool
