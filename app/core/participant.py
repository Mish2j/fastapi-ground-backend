from dataclasses import dataclass, field
from datetime import datetime, timezone
import random
import string

from app.constants import Command, ParticipantRole


COMMAND_PERMISSIONS = {
    ParticipantRole.FLIGHT_DIRECTOR: {
        Command.SET_MODE,
        Command.SET_DOWNLINK_RATE,
        Command.INJECT_FAULT,
        Command.CLEAR_FAULTS,
    },
    ParticipantRole.GROUND_OPERATOR: {
        Command.SET_MODE,
        Command.SET_DOWNLINK_RATE,
        Command.CLEAR_FAULTS,
    },
    ParticipantRole.TELEMETRY_OFFICER: set(),
    ParticipantRole.PAYLOAD_OFFICER: set(),
    ParticipantRole.OBSERVER: set(),
}


def generate_participant_id() -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


@dataclass
class Participant:
    display_name: str
    role: ParticipantRole = ParticipantRole.OBSERVER
    participant_id: str = field(default_factory=generate_participant_id)
    is_connected: bool = False  # OR maybe assign room code (if no room assigned, then part. is disconnected)
    joined_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def connect(self) -> None:
        self.is_connected = True

    def disconnect(self) -> None:
        self.is_connected = False

    def update_display_name(self, display_name: str) -> None:
        if not display_name.strip():
            raise ValueError('Display name cannot be empty')

        self.display_name = display_name.strip()

    def update_role(self, role: ParticipantRole) -> None:
        self.role = role

    def can_execute(self, command: Command) -> bool:
        """Command permissions by role"""
        return command in COMMAND_PERMISSIONS[self.role]

    def can_assign_roles(self) -> bool:
        return self.role == ParticipantRole.FLIGHT_DIRECTOR

    def can_view_payload(self) -> bool:
        return self.role in {
            ParticipantRole.FLIGHT_DIRECTOR,
            ParticipantRole.PAYLOAD_OFFICER,
        }
