from enum import StrEnum

ERR_ROOM_NOT_FOUND = 'Room not found!'
ERR_PARTICIPANT_NOT_FOUND = 'Participant not found!'

ROOM_CLEANUP_INTERVAL_SECONDS = 60
ROOM_INACTIVITY_TIMEOUT_MINUTES = 30

SIMULATION_STEP_SECONDS = 1


class FaultType(StrEnum):
    BATTERY_DEGRADATION = 'BATTERY_DEGRADATION'
    LOW_BATTERY = 'LOW_BATTERY'
    SOLAR_PANEL_FAILURE = 'SOLAR_PANEL_FAILURE'
    HIGH_TEMPERATURE = 'HIGH_TEMPERATURE'
    ANTENNA_FAILURE = 'ANTENNA_FAILURE'
    GPS_FAILURE = 'GPS_FAILURE'
    STAR_TRACKER_FAILURE = 'STAR_TRACKER_FAILURE'
    REACTION_WHEEL_FAILURE = 'REACTION_WHEEL_FAILURE'
    MEMORY_ERROR = 'MEMORY_ERROR'
    CPU_OVERLOAD = 'CPU_OVERLOAD'
    THRUSTER_FAILURE = 'THRUSTER_FAILURE'


class FaultSeverity(StrEnum):
    INFO = 'INFO'
    WARNING = 'WARNING'
    CRITICAL = 'CRITICAL'


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
