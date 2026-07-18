from fastapi import APIRouter, HTTPException

# from app.services.event_service import get_events
from app.services.room_service import room_manager
from app.constants import ERR_ROOM_NOT_FOUND

router = APIRouter(prefix='/rooms/{room_code}/events', tags=['Events'])


@router.get('')
def events(room_code: str, limit: int = 50):
    room = room_manager.get_room(room_code)

    if room is None:
        raise HTTPException(status_code=404, detail=ERR_ROOM_NOT_FOUND)

    return room.get_events(limit)
