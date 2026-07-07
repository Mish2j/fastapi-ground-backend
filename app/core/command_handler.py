from pydantic import ValidationError

from app.core.satellite_state import (
    update_mode,
    update_downlink_rate,
    add_faults,
    clear_faults,
)

from app.constants import Status
from app.models.command import SetModeParams, SetDownlinkRateParams, InjectFaultParams


def handle_set_mode(params: dict):
    try:
        validated_mode_params = SetModeParams(**params)
    except ValidationError as error:
        return {
            'status': Status.REJECTED,
            # 'message': f'Invalid mode: {mode}',
            'message': str(error),
        }

    update_mode(validated_mode_params.mode)

    return {
        'status': Status.ACCEPTED,
        'message': f'Mode changed to {validated_mode_params.mode}',
    }


def handle_set_downlink_rate(params: dict):
    try:
        validated_downlink_rate = SetDownlinkRateParams(**params)
    except ValidationError as error:
        return {
            'status': Status.REJECTED,
            # 'message': f'Invalid downlink rate: {rate}',
            'message': str(error),
        }

    update_downlink_rate(validated_downlink_rate.rate)

    return {
        'status': Status.ACCEPTED,
        'message': f'Downlink rate changed to {validated_downlink_rate.rate}',
    }


def handle_add_fault(params: dict):
    try:
        validated_fault = InjectFaultParams(**params)
    except ValidationError as error:
        return {
            'status': Status.REJECTED,
            # 'message': 'Fault name is required',
            'message': str(error),
        }

    add_faults(validated_fault.fault)

    return {
        'status': Status.ACCEPTED,
        'message': f'Fault injected: {validated_fault.fault}',
    }


def handle_clear_faults():
    clear_faults()

    return {
        'status': Status.ACCEPTED,
        'message': 'All faults cleared',
    }
