from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from pydantic import ValidationError

from app.constants import Command, ParticipantRole, Status
from app.core.events.event import Event
from app.core.events.event_types import EventStatus, EventType
from app.core.faults.fault import Fault
from app.core.faults.fault_types import FaultSeverity, FaultType
from app.core.mission_state import MissionState
from app.core.participant import Participant
from app.core.room import MissionRoom
from app.models.command import (
    ClearFaultParams,
    CommandRequest,
    CommandResponse,
    InjectFaultParams,
    SetDownlinkRateParams,
    SetModeParams,
)
from app.services.event_service import event_service

COMMAND_PERMISSIONS = {
    ParticipantRole.FLIGHT_DIRECTOR: {
        Command.SET_MODE,
        Command.SET_DOWNLINK_RATE,
        Command.INJECT_FAULT,
        Command.CLEAR_ALL_FAULTS,
        Command.CLEAR_FAULT,
    },
    ParticipantRole.GROUND_OPERATOR: {
        Command.SET_MODE,
        Command.SET_DOWNLINK_RATE,
        Command.CLEAR_ALL_FAULTS,
        Command.CLEAR_FAULT,
    },
    ParticipantRole.TELEMETRY_OFFICER: set(),
    ParticipantRole.PAYLOAD_OFFICER: set(),
    ParticipantRole.OBSERVER: set(),
}


@dataclass
class CommandService:
    def execute(
        self,
        room: MissionRoom,
        participant: Participant,
        request: CommandRequest,
    ) -> CommandResponse:

        # verify participant before running command
        if participant is None:
            return CommandResponse(
                status=Status.REJECTED,
                message='Participant not found',
            )

        if not participant.is_connected:
            return CommandResponse(
                status=Status.REJECTED,
                message='Participant is not connected',
            )

        if not self.can_execute(request.command, participant):
            return CommandResponse(
                status=Status.REJECTED,
                message=f'{participant.role.value} is not allowed to execute {request.command}',
            )

        command = request.command
        params = request.params

        if command == Command.SET_MODE:
            result = self.__handle_set_mode(params, room.mission_state)

        elif command == Command.SET_DOWNLINK_RATE:
            result = self.__handle_set_downlink_rate(params, room.mission_state)

        elif command == Command.INJECT_FAULT:
            result = self.__handle_inject_fault(params, room.mission_state)

        elif command == Command.CLEAR_ALL_FAULTS:
            result = self.__handle_clear_all_faults(room.mission_state)

        elif command == Command.CLEAR_FAULT:
            result = self.__handle_clear_fault(
                room.mission_state,
                params,
            )

        else:
            result = CommandResponse(
                status=Status.REJECTED,
                message=f'Unknown command: {command}',
            )

        event = Event(
            timestamp=datetime.now(UTC),
            type=EventType.COMMAND,
            status=EventStatus(result.status),
            message=f'{participant.display_name}: {result.message}',
            command=command,
        )

        event_service.add_event(room, event)

        room.touch()

        return result

    def can_execute(self, command: Command, participant: Participant) -> bool:
        """Command permissions by role"""
        return command in COMMAND_PERMISSIONS[participant.role]

    def __handle_set_mode(
        self, params: dict, mission_state: MissionState
    ) -> CommandResponse:
        try:
            validated = SetModeParams(**params)
        except ValidationError as error:
            return CommandResponse(
                status=Status.REJECTED,
                message=str(error),
            )

        mission_state.set_mode(validated.mode)

        return CommandResponse(
            status=Status.ACCEPTED,
            message=f'Mode changed to {validated.mode}',
        )

    def __handle_set_downlink_rate(
        self, params: dict, mission_state: MissionState
    ) -> CommandResponse:
        try:
            validated = SetDownlinkRateParams(**params)
        except ValidationError as error:
            return CommandResponse(
                status=Status.REJECTED,
                message=str(error),
            )

        mission_state.set_downlink_rate(validated.rate)

        return CommandResponse(
            status=Status.ACCEPTED,
            message=f'Downlink rate changed to {validated.rate}',
        )

    def __handle_inject_fault(
        self, params: dict, mission_state: MissionState
    ) -> CommandResponse:
        try:
            validated = InjectFaultParams(**params)
        except ValidationError as error:
            return CommandResponse(
                status=Status.REJECTED,
                message=str(error),
            )

        fault = Fault(
            id=str(uuid4()),
            type=validated.fault_type,
            severity=FaultSeverity.WARNING,
            message=f'{validated.fault_type} injected',
            created_at=datetime.now(UTC),
        )

        mission_state.inject_fault(fault)

        return CommandResponse(
            status=Status.ACCEPTED,
            message=f'Fault injected: {validated.fault_type}',
        )

    def __handle_clear_all_faults(self, mission_state: MissionState) -> CommandResponse:
        mission_state.clear_all_faults()

        return CommandResponse(
            status=Status.ACCEPTED,
            message='All faults cleared',
        )

    def __handle_clear_fault(
        self,
        mission_state: MissionState,
        params: dict,
    ) -> CommandResponse:
        try:
            validated = ClearFaultParams(**params)
        except ValidationError as error:
            return CommandResponse(
                status=Status.REJECTED,
                message=str(error),
            )
        mission_state.clear_fault(validated.fault_type)

        return CommandResponse(
            status=Status.ACCEPTED,
            message=f'Fault cleared: {validated.fault_type}',
        )


command_service = CommandService()
