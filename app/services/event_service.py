from dataclasses import dataclass

from app.core.events.event import Event
from app.core.mission_state import MissionState
from app.core.room import MissionRoom


@dataclass
class EventService:
    MAX_EVENT_LOG: int = 200

    def collect_events(
        self,
        mission_state: MissionState,
        room: MissionRoom,
    ) -> None:
        """Collects events from the mission state and adds them to the room's event log."""

        if not mission_state.pending_events:
            return

        events = mission_state.pending_events

        self.__trim(room, len(events))

        room.event_log.extend(events)

        # Clear the pending events after collecting them
        mission_state.pending_events.clear()

    def add_event(self, room: MissionRoom, event: Event) -> None:
        """Adds a single event to the room's event log."""
        # Limit the number of events in the room's event log
        self.__trim(room, 1)

        room.event_log.append(event)

    def __trim(self, room: MissionRoom, new_event_count: int) -> None:
        """Trims the event log to make space for pending events."""
        excess_count = len(room.event_log) + new_event_count - self.MAX_EVENT_LOG

        if excess_count > 0:
            del room.event_log[:excess_count]


event_service = EventService()
