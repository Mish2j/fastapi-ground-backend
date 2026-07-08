from dataclasses import dataclass, field
from datetime import datetime, timezone
from fastapi import WebSocket

from app.constants import DownlinkRate, Mode


@dataclass
class MissionRoom:
    room_code: str
    name: str
    max_users: int
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    satellite_state: dict = field(
        default_factory=lambda: {
            'satellite_id': 'SAT-001',
            'mode': Mode.NOMINAL,
            'downlink_rate': DownlinkRate.LOW,
            'faults': [],
        }
    )
    telemetry_history: list[dict] = field(default_factory=list)
    event_log: list[dict] = field(default_factory=list)
    participants: dict[str, str] = field(default_factory=dict)
    connections: list[WebSocket] = field(default_factory=list)
