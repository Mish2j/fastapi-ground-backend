from app.models.command import CommandRequest
from app.core.command_handler import handle_set_mode, handle_set_downlink_rate, handle_add_fault, handle_clear_faults
from app.services.event_service import add_event


def execute_command(request: CommandRequest):
    # "SET_MODE"
    # "SET_DOWNLINK_RATE"
    # "INJECT_FAULT"
    # "CLEAR_FAULTS"
    pass