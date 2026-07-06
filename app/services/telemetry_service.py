from app.core.simulator import generate_telemetry
from app.storage.memory_store import (
    save_telemetry,
    get_latest_telemetry,
    get_telemetry_history,
)


def create_new_telemetry():
    telemetry = generate_telemetry()
    save_telemetry(telemetry)
    return telemetry


def get_latest():
    latest = get_latest_telemetry()

    # if latest is None:
    #     return create_new_telemetry()

    return latest


def get_history(limit: int = 100):
    return get_telemetry_history(limit)
