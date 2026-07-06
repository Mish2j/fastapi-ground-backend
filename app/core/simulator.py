from datetime import datetime, timezone
import random

from app.core.satellite_state import get_satellite_state


def generate_telemetry():
    state = get_satellite_state()

    telemetry = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'satellite_id': state['satellite_id'],
        'mode': state['mode'],
        'downlink_rate': state['downlink_rate'],
        'battery_voltage': round(random.uniform(27.5, 29.0), 2),
        'temperature_c': round(random.uniform(18.0, 32.0), 2),
        'signal_db': round(random.uniform(-90, -60), 2),
        'latitude': round(random.uniform(-60, 60), 4),
        'longitude': round(random.uniform(-180, 180), 4),
        'faults': state['faults'],
    }

    return telemetry
