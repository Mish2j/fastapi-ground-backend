from app.core.satellite_state import (
    update_mode,
    update_downlink_rate,
    add_faults,
    clear_faults,
)

from app.constants import Mode as ALLOWED_MODES, DownlinkRate, Status


def handle_set_mode(params: dict):
    mode = params.get('mode')

    if mode not in ALLOWED_MODES.__members__:
        return {
            'status': Status.REJECTED,
            'message': f'Invalid mode: {mode}',
        }

    update_mode(mode)

    return {
        'status': Status.ACCEPTED,
        'message': f'Mode changed to {mode}',
    }


def handle_set_downlink_rate(params: dict):
    rate = params.get('rate')

    if rate not in DownlinkRate.__members__:
        return {
            'status': Status.REJECTED,
            'message': f'Invalid downlink rate: {rate}',
        }

    update_downlink_rate(rate)

    return {
        'status': Status.ACCEPTED,
        'message': f'Downlink rate changed to {rate}',
    }


def handle_add_fault(params: dict):
    fault = params.get('fault')

    if not fault:
        return {
            'status': Status.REJECTED,
            'message': 'Fault name is required',
        }

    add_faults(fault)

    return {
        'status': Status.ACCEPTED,
        'message': f'Fault injected: {fault}',
    }


def handle_clear_faults():
    clear_faults()

    return {
        'status': Status.ACCEPTED,
        'message': 'All faults cleared',
    }
