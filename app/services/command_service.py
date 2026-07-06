from app.models.command import CommandRequest
from app.core.command_handler import (
    handle_set_mode,
    handle_set_downlink_rate,
    handle_add_fault,
    handle_clear_faults,
)
from app.services.event_service import add_event
from app.constants import Status, Command, Event


def execute_command(request: CommandRequest):
    command = request.command
    params = request.params

    if command == Command.SET_MODE:
        result = handle_set_mode(params)

    elif command == Command.SET_DOWNLINK_RATE:
        result = handle_set_downlink_rate(params)

    elif command == Command.INJECT_FAULT:
        result = handle_add_fault(params)

    elif command == Command.CLEAR_FAULTS:
        result = handle_clear_faults()

    else:
        result = {
            'status': Status.REJECTED,
            'message': f'Unknown command: {command}',
        }

    add_event(
        event_type=Event.COMMAND,
        command=command,
        status=result['status'],
        message=result['message'],
    )

    return result
