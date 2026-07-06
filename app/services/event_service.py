from datetime import datetime, timezone

from app.storage.memory_store import save_event, get_event_log


def add_event(
    event_type: str, message: str, status: str = 'INFO', command: str | None = None
):
    event = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'type': event_type,
        'status': status,
        'message': message,
        'command': command,
    }

    save_event(event)
    return event


def get_events(limit: int = 50):
    return get_event_log(limit)
