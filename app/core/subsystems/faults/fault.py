from datetime import datetime

from pydantic import BaseModel

from app.constants import FaultSeverity, FaultType


class Fault(BaseModel):
    id: str
    type: FaultType
    severity: FaultSeverity
    message: str
    created_at: datetime
    active: bool = True
