from app.core.satellite_state import get_Satellite_state, update_mode, update_downlink_rate, add_faults, clear_faults

from constants import ALLOWED_MODES, STATUS_REJECT, STATUS_ACCEPT

'''
    add_event(
        event_type=EVENT_COMMAND,
        command=SET_MODE_COMMAND,
        status=STATUS_ACCEPT,
        message=result["message"]
    )
'''

def handle_set_mode(params: dict):
    mode = params.get("mode")

    if mode not in ALLOWED_MODES:
        return {
            "status": STATUS_REJECT,
            "message": f"Invalid mode: {mode}"
        }
    
    update_mode(mode)

    return {
        "status": STATUS_ACCEPT,
        "message": f"Mode changed to {mode}"
    }


def handle_set_downlink_rate(params: dict):
    pass


def handle_add_fault(params: dict):
    pass


def handle_clear_faults():
    pass