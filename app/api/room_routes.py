# POST /rooms
# GET  /rooms/{room_code}
# POST /rooms/{room_code}/join
# GET  /rooms/{room_code}/telemetry/latest
# GET  /rooms/{room_code}/telemetry/history
# GET  /rooms/{room_code}/events
# POST /rooms/{room_code}/commands
# WS   /ws/rooms/{room_code}/telemetry


from fastapi import APIRouter, HTTPException, WebSocket

from app.models.room import RoomResponse, JoinRoomRequest, CreateRoomRequest
from app.services.room_service import create_room, get_room, join__room


router = APIRouter(prefix='/rooms', tags=['Rooms'])


@router.post('', response_model=RoomResponse)
def create_new_room(request: CreateRoomRequest):
    return create_room(request)


@router.post('/{room_code}/join', response_model=RoomResponse)
def join_existing_room(room_code: str, request: JoinRoomRequest):
    try:
        room_response = join__room(room_code, request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    if room_response is None:
        raise HTTPException(status_code=404, detail='Room not found!')

    return room_response
