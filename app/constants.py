from enum import StrEnum

ERR_ROOM_NOT_FOUND = 'Room not found!'

ROOM_CLEANUP_INTERVAL_SECONDS = 60
ROOM_INACTIVITY_TIMEOUT_MINUTES = 30


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


class ParticipantRole(StrEnum):
    FLIGHT_DIRECTOR = (
        'Flight Director'  # create/manage room, assign roles, send commands
    )
    GROUND_OPERATOR = 'Ground Operator'  # send spacecraft commands
    TELEMETRY_OFFICER = (
        'Telemetry Officer'  # view telemetry/events, maybe acknowledge faults later
    )
    PAYLOAD_OFFICER = 'Payload Officer'  # send payload/science commands later
    OBSERVER = 'Observer'  # view only
