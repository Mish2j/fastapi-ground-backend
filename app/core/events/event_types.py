from enum import StrEnum


class EventType(StrEnum):
    COMMAND = 'COMMAND'
    FAULT = 'FAULT'
    MODE_CHANGE = 'MODE_CHANGE'
    WARNING = 'WARNING'
    SYSTEM = 'SYSTEM'


class EventStatus(StrEnum):
    INFO = 'INFO'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
