from fastapi import APIRouter, HTTPException

from app.constants import ERR_ROOM_NOT_FOUND
from app.managers.room_manager import room_manager

router = APIRouter(prefix='/rooms/{room_code}/events', tags=['Events'])


@router.get('')
def events(room_code: str, limit: int = 50):
    room = room_manager.get_room(room_code)

    if room is None:
        raise HTTPException(status_code=404, detail=ERR_ROOM_NOT_FOUND)

    return room.get_events(limit)
