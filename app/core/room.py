from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from app.constants import ERR_PARTICIPANT_NOT_FOUND, ParticipantRole
from app.core.participant import Participant
from app.core.state import MissionState
from app.models.telemetry import Telemetry

MAX_TELEMETRY_HISTORY = 500
MAX_EVENT_LOG = 200

ROLE_LIMITS: dict[ParticipantRole, int | None] = {
    ParticipantRole.FLIGHT_DIRECTOR: 1,
    ParticipantRole.GROUND_OPERATOR: 2,
    ParticipantRole.TELEMETRY_OFFICER: 2,
    ParticipantRole.PAYLOAD_OFFICER: 1,
    ParticipantRole.OBSERVER: None,  # unlimited up to max_users
}


@dataclass
class MissionRoom:
    room_code: str
    name: str
    max_users: int
    telemetry_history: list[Telemetry] = field(default_factory=list)
    last_activity_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    mission_state: MissionState = field(default_factory=MissionState)
    event_log: list[dict] = field(default_factory=list)
    # event_log: list[MissionEvent]
    participants: dict[str, Participant] = field(default_factory=dict)

    def connected_users(self) -> int:
        return sum(
            1 for participant in self.participants.values() if participant.is_connected
        )

    def has_connected_users(self) -> bool:
        return self.connected_users() > 0

    # TODO: The name is a little misleading. (can be participant_count)
    def active_users(self) -> int:
        return len(
            self.participants
        )  # this is participants in the room, not necessarily active

    def get_participant(self, participant_id: str) -> Participant | None:
        return self.participants.get(participant_id)

    def __require_participant(self, participant_id: str) -> Participant:
        participant = self.get_participant(participant_id)

        if participant is None:
            raise ValueError(ERR_PARTICIPANT_NOT_FOUND)

        return participant

    # TODO: handle rejoin
    def join(self, display_name: str) -> Participant:
        if self.active_users() >= self.max_users:
            raise ValueError('Room is full')

        participant = Participant(display_name=display_name)

        # first person = FLIGHT_DIRECTOR
        if self.active_users() == 0:
            participant.update_role(ParticipantRole.FLIGHT_DIRECTOR)

        participant.connect()

        self.participants[participant.participant_id] = participant

        self.touch()

        return participant

    def disconnect_participant(self, participant_id: str) -> Participant:
        participant = self.__require_participant(participant_id)

        participant.disconnect()
        self.touch()

        return participant

    def remove_participant(self, participant_id: str) -> Participant:
        participant = self.disconnect_participant(participant_id)
        self.participants.pop(participant_id)

        return participant

    def save_telemetry(self, telemetry: Telemetry):
        if len(self.telemetry_history) >= MAX_TELEMETRY_HISTORY:
            self.telemetry_history.pop(0)

        self.telemetry_history.append(telemetry)

    def get_latest_telemetry(self) -> Telemetry | None:
        if not self.telemetry_history:
            # May want to generate and return telemetry instead: return self.generate_telemetry()
            return None

        return self.telemetry_history[-1]

    def get_telemetry_history(self, limit: int = 100) -> list[Telemetry]:
        return self.telemetry_history[-limit:]

    def save_event(self, event: dict):
        if len(self.event_log) >= MAX_EVENT_LOG:
            self.event_log.pop(0)

        self.event_log.append(event)

    def add_event(
        self,
        event_type: str,
        message: str,
        status: str = 'INFO',
        command: str | None = None,
    ) -> dict:
        event = {
            'timestamp': datetime.now(UTC).isoformat(),
            'type': event_type,
            'status': status,
            'message': message,
            'command': command,
        }

        self.save_event(event)

        return event

    def get_events(self, limit: int = 50) -> list[dict]:
        return self.event_log[-limit:]

    # Flight Director assigns roles manually
    def assign_role(
        self, requester_id: str, participant_id: str, new_role: ParticipantRole
    ) -> Participant:
        self.touch()
        requester = self.participants.get(requester_id)
        participant = self.participants.get(participant_id)

        if requester is None:
            raise ValueError('Requester not found')

        if participant is None:
            raise ValueError(ERR_PARTICIPANT_NOT_FOUND)

        if requester.participant_id == participant_id:
            raise ValueError('Flight Director cannot assign role to themselves')

        if not requester.can_assign_roles():
            raise ValueError('Only Flight Director can assign roles')

        # if the participant already has the requested role, do nothing
        if participant.role == new_role:
            return participant

        if new_role == ParticipantRole.FLIGHT_DIRECTOR and any(
            p.role == ParticipantRole.FLIGHT_DIRECTOR
            for p in self.participants.values()
        ):
            raise ValueError('Room already has a Flight Director')

        limit = ROLE_LIMITS[new_role]
        if limit is not None:
            current_count = sum(
                1 for p in self.participants.values() if p.role == new_role
            )
            if current_count >= limit:
                raise ValueError(f'Role limit reached for {new_role}')

        participant.update_role(new_role)
        return participant

    def is_inactive(self, timeout_minutes: int = 30) -> bool:
        if self.has_connected_users():
            return False

        cutoff = datetime.now(UTC) - timedelta(minutes=timeout_minutes)
        return self.last_activity_at < cutoff

    def touch(self) -> None:
        self.last_activity_at = datetime.now(UTC)
