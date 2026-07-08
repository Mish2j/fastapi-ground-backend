import random
import string
from app.models.room import CreateRoomRequest, JoinRoomRequest, RoomResponse
from app.core.room import MissionRoom

rooms: dict[str, MissionRoom] = {}


def generate_room_code() -> str:
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        if code not in rooms:
            return code


def create_room(request: CreateRoomRequest) -> RoomResponse:
    room_code = generate_room_code()

    room = MissionRoom(
        room_code=room_code,
        name=request.name,
        max_users=request.max_users,
    )

    rooms[room_code] = room

    return to_room_response(room)


def get_room(room_code: str) -> MissionRoom | None:
    return rooms.get(room_code.upper())


def join__room(room_code: str, request: JoinRoomRequest) -> RoomResponse | None:
    room = get_room(room_code)

    if room is None:
        return None

    if len(room.participants) >= room.max_users:
        raise ValueError('Room is full')

    participant_id = ''.join(
        random.choices(string.ascii_lowercase + string.digits, k=8)
    )
    room.participants[participant_id] = request.display_name

    return to_room_response(room)


def to_room_response(room: MissionRoom) -> RoomResponse:
    return RoomResponse(
        room_code=room.room_code,
        name=room.name,
        max_users=room.max_users,
        active_users=len(room.participants),
    )
