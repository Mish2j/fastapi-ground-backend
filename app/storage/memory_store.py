telemetry_history = []
event_log = []
MAX_TELEMETRY_HISTORY = 500
MAX_EVENT_LOG = 200


def save_telemetry(telemetry: dict):
    telemetry_history.append(telemetry)

    if len(telemetry_history) > MAX_TELEMETRY_HISTORY:
        telemetry_history.pop(0)


def get_latest_telemetry():
    if not telemetry_history:
        return None
    
    return telemetry_history[-1]


def get_telemetry_history(limit: int = 100):
    return telemetry_history[-limit:]


def save_event(event: dict):
    if len(event_log) > MAX_EVENT_LOG:
        event_log.pop(0)
    
    event_log.append(event)


def get_event_log(limit: int = 50):
    return event_log[-limit:]