from typing import Final
from enum import StrEnum

STATUS_REJECT: Final = "REJECTED"
STATUS_ACCEPT: Final = "ACCEPTED"


SET_MODE_COMMAND: Final = "SET_MODE"

EVENT_COMMAND: Final = "COMMAND"


class Mode(StrEnum):
    NOMINAL = "NOMINAL"
    SAFE = "SAFE"
    SCIENCE = "SCIENCE"

class DownlinkRate(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"