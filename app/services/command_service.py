from dataclasses import dataclass

from pydantic import ValidationError

from app.constants import Command, Event, ParticipantRole, Status
from app.core.participant import Participant
from app.core.room import MissionRoom
from app.core.state import MissionState
from app.models.command import (
    CommandRequest,
    CommandResponse,
    InjectFaultParams,
    SetDownlinkRateParams,
    SetModeParams,
)

COMMAND_PERMISSIONS = {
    ParticipantRole.FLIGHT_DIRECTOR: {
        Command.SET_MODE,
        Command.SET_DOWNLINK_RATE,
        Command.INJECT_FAULT,
        Command.CLEAR_FAULTS,
    },
    ParticipantRole.GROUND_OPERATOR: {
        Command.SET_MODE,
        Command.SET_DOWNLINK_RATE,
        Command.CLEAR_FAULTS,
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

        elif command == Command.CLEAR_FAULTS:
            result = self.__handle_clear_faults(room.mission_state)

        else:
            result = CommandResponse(
                status=Status.REJECTED,
                message=f'Unknown command: {command}',
            )

        room.add_event(
            event_type=Event.COMMAND,
            command=command,
            status=result.status,
            message=f'{participant.display_name}: {result.message}',
        )

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

        mission_state.inject_fault(validated.fault)

        return CommandResponse(
            status=Status.ACCEPTED,
            message=f'Fault injected: {validated.fault}',
        )

    def __handle_clear_faults(self, mission_state: MissionState) -> CommandResponse:
        mission_state.clear_faults()

        return CommandResponse(
            status=Status.ACCEPTED,
            message='All faults cleared',
        )


command_service = CommandService()
