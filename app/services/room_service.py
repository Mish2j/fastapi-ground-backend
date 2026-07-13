from dataclasses import dataclass, field
import random
import string
from app.models.room import CreateRoomRequest, JoinRoomRequest, RoomResponse
from app.core.room import MissionRoom


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

    def __generate_participant_id(self) -> str:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

    def to_room_response(self, room: MissionRoom) -> RoomResponse:
        return RoomResponse(
            room_code=room.room_code,
            name=room.name,
            max_users=room.max_users,
            active_users=len(room.participants),
        )

    def join__room(
        self, room_code: str, request: JoinRoomRequest
    ) -> RoomResponse | None:
        room = self.get_room(room_code)

        if room is None:
            return None

        if len(room.participants) >= room.max_users:
            raise ValueError('Room is full')

        participant_id = self.__generate_participant_id()
        room.join(participant_id, request.display_name)

        return self.to_room_response(room)


room_manager = RoomManager()
