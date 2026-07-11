from fastapi import APIRouter, HTTPException

from app.models.room import RoomResponse, JoinRoomRequest, CreateRoomRequest
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


@router.post('/{room_code}/join', response_model=RoomResponse)
def join_existing_room(room_code: str, request: JoinRoomRequest):
    try:
        room_response = room_manager.join__room(room_code, request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    if room_response is None:
        raise HTTPException(status_code=404, detail=ERR_ROOM_NOT_FOUND)

    return room_response
