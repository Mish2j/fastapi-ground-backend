from datetime import datetime

from pydantic import BaseModel

from app.core.faults.fault_types import FaultSeverity, FaultType


class Fault(BaseModel):
    id: str
    type: FaultType
    severity: FaultSeverity
    message: str
    created_at: datetime
    active: bool = True
