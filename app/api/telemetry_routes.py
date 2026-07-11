from fastapi import APIRouter, HTTPException

# from app.services.telemetry_service import get_latest, get_history
from app.services.room_service import room_manager
from app.constants import ERR_ROOM_NOT_FOUND

router = APIRouter(prefix='/rooms/{room_code}/telemetry', tags=['Telemetry'])


@router.get('/latest')
def latest_telemetry(room_code: str):
    room = room_manager.get_room(room_code)

    if room is None:
        raise HTTPException(status_code=404, detail=ERR_ROOM_NOT_FOUND)

    return room.get_latest_telemetry()


@router.get('/history')
def telemetry_history(room_code: str, limit: int = 100):
    room = room_manager.get_room(room_code)

    if room is None:
        raise HTTPException(status_code=404, detail=ERR_ROOM_NOT_FOUND)

    return room.get_telemetry_history(limit)
