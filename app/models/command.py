from pydantic import BaseModel, Field
from typing import Any

from app.constants import DownlinkRate, Mode


class CommandRequest(BaseModel):
    command: str
    params: dict[str, Any] = Field(default_factory=dict)


class CommandResponse(BaseModel):
    status: str
    message: str


class SetModeParams(BaseModel):
    mode: Mode


class SetDownlinkRateParams(BaseModel):
    rate: DownlinkRate


class InjectFaultParams(BaseModel):
    fault: str = Field(min_length=1)
