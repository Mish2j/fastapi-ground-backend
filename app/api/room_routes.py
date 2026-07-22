from fastapi import APIRouter, HTTPException

from app.models.room import (
    JoinRoomResponse,
    RoomResponse,
    JoinRoomRequest,
    CreateRoomRequest,
)
from app.services.room_service import room_manager

from app.constants import ERR_ROOM_NOT_FOUND


router = APIRouter(prefix='/rooms', tags=['Rooms'])


@router.post('', response_model=RoomResponse)
def create_new_room(request: CreateRoomRequest):
    return room_manager.create_room(request)


@router.get('/{room_code}', response_model=RoomResponse)
def get_room_info(room_code: str):
    room = room_manager.get_room(room_code)

    if room is None:
        raise HTTPException(status_code=404, detail=ERR_ROOM_NOT_FOUND)

    return room_manager.to_room_response(room)


@router.post('/{room_code}/join', response_model=JoinRoomResponse)
def join_existing_room(room_code: str, request: JoinRoomRequest) -> JoinRoomResponse:
    try:
        room_response = room_manager.join_room(room_code, request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    if room_response is None:
        raise HTTPException(status_code=404, detail=ERR_ROOM_NOT_FOUND)

    return room_response


@router.get('')
def list_rooms():
    return [
        {
            'room_code': room.room_code,
            'name': room.name,
            'max_users': room.max_users,
            'connected_users': room.connected_users(),
            'total_participants': len(room.participants),
            'is_streaming': room.is_streaming,
            'last_activity_at': room.last_activity_at.isoformat(),
            'is_inactive': room.is_inactive(),
        }
        for room in room_manager.list_rooms()
    ]


@router.delete('/inactive')
def cleanup_inactive_rooms(timeout_minutes: int = 30) -> dict:
    removed_rooms = room_manager.cleanup_inactive_rooms(timeout_minutes)

    return {
        'removed_count': len(removed_rooms),
        'removed_rooms': removed_rooms,
    }
