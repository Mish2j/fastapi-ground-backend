from typing import Any

from pydantic import BaseModel, Field

from app.constants import Command, DownlinkRate, Mode
from app.core.faults.fault_types import FaultType


class CommandRequest(BaseModel):
    participant_id: str
    command: Command
    params: dict[str, Any] = Field(default_factory=dict)


class CommandResponse(BaseModel):
    status: str
    message: str


class SetModeParams(BaseModel):
    mode: Mode


class SetDownlinkRateParams(BaseModel):
    rate: DownlinkRate


class InjectFaultParams(BaseModel):
    fault_type: FaultType


class ClearFaultParams(BaseModel):
    fault_type: FaultType
