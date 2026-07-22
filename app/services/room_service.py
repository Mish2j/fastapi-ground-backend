from dataclasses import dataclass, field
import random
import string
from app.models.room import (
    CreateRoomRequest,
    JoinRoomRequest,
    JoinRoomResponse,
    RoomResponse,
)
from app.core.room import MissionRoom

from app.constants import ROOM_INACTIVITY_TIMEOUT_MINUTES


@dataclass
class RoomManager:
    rooms: dict[str, MissionRoom] = field(default_factory=dict)

    def __generate_room_code(self) -> str:
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

            if code not in self.rooms:
                return code

    def create_room(self, request: CreateRoomRequest) -> RoomResponse:
        room_code = self.__generate_room_code()

        room = MissionRoom(
            room_code=room_code,
            name=request.name,
            max_users=request.max_users,
        )

        self.rooms[room_code] = room

        return self.to_room_response(room)

    def get_room(self, room_code: str) -> MissionRoom | None:
        return self.rooms.get(room_code.upper())

    def to_room_response(self, room: MissionRoom) -> RoomResponse:
        return RoomResponse(
            room_code=room.room_code,
            name=room.name,
            max_users=room.max_users,
            active_users=len(room.participants),
        )

    def join_room(
        self, room_code: str, request: JoinRoomRequest
    ) -> RoomResponse | None:
        room = self.get_room(room_code)

        if room is None:
            return None

        participant = room.join(request.display_name)

        return JoinRoomResponse(
            room_code=room.room_code,
            name=room.name,
            max_users=room.max_users,
            active_users=room.active_users(),
            participant_id=participant.participant_id,
            role=participant.role,
        )

    def list_rooms(self) -> list[MissionRoom]:
        return list(self.rooms.values())

    def cleanup_inactive_rooms(self, timeout_minutes: int = 30) -> list[str]:
        inactive_room_codes = [
            room_code
            for room_code, room in self.rooms.items()
            if room.is_inactive(timeout_minutes)
        ]

        for room_code in inactive_room_codes:
            room = self.rooms[room_code]

            if room.is_streaming:
                # room.stop_stream()
                room.is_streaming = False

            del self.rooms[room_code]

        return inactive_room_codes


room_manager = RoomManager()
