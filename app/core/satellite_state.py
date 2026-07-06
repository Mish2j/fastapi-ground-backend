from app.constants import DownlinkRate, Mode

satellite_state = {
    'satellite_id': 'SAT-001',
    'mode': Mode.NOMINAL,
    'downlink_rate': DownlinkRate.LOW,
    'faults': [],
}


def get_satellite_state():
    return satellite_state


def update_mode(mode: str):
    satellite_state['mode'] = mode


def update_downlink_rate(rate: str):
    satellite_state['downlink_rate'] = rate


def add_faults(fault: str):
    satellite_state['faults'].append(fault)


def clear_faults():
    satellite_state['faults'].clear()
