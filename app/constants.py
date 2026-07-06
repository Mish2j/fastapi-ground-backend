from enum import StrEnum


class Status(StrEnum):
    REJECTED = 'REJECTED'
    ACCEPTED = 'ACCEPTED'


class Event(StrEnum):
    COMMAND = 'COMMAND'
    SYSTEM = 'SYSTEM'
    FAULT = 'FAULT'


class Command(StrEnum):
    SET_MODE = 'SET_MODE'
    SET_DOWNLINK_RATE = 'SET_DOWNLINK_RATE'
    INJECT_FAULT = 'INJECT_FAULT'
    CLEAR_FAULTS = 'CLEAR_FAULTS'


class Mode(StrEnum):
    NOMINAL = 'NOMINAL'
    SAFE = 'SAFE'
    SCIENCE = 'SCIENCE'


class DownlinkRate(StrEnum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
