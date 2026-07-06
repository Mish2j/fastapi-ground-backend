from app.models.command import CommandRequest
from app.core.command_handler import (
    handle_set_mode,
    handle_set_downlink_rate,
    handle_add_fault,
    handle_clear_faults,
)
from app.services.event_service import add_event
from constants import STATUS_REJECT


def execute_command(request: CommandRequest):
    command = request.command
    params = request.params

    if command == 'SET_MODE':
        result = handle_set_mode(params)

    elif command == 'SET_DOWNLINK_RATE':
        result = handle_set_downlink_rate(params)

    elif command == 'INJECT_FAULT':
        result = handle_add_fault(params)

    elif command == 'CLEAR_FAULTS':
        result = handle_clear_faults()

    else:
        result = {
            'status': STATUS_REJECT,
            'message': f'Unknown command: {command}',
        }

    add_event(
        event_type='COMMAND',
        command=command,
        status=result['status'],
        message=result['message'],
    )

    return result
