from fastapi import APIRouter, HTTPException

from app.models.command import CommandRequest
# from app.services.command_service import execute_command

from app.services.room_service import room_manager
from app.constants import ERR_ROOM_NOT_FOUND

router = APIRouter(prefix='/rooms/{room_code}/commands', tags=['Commands'])


@router.post('')
def send_command(room_code: str, request: CommandRequest):
    room = room_manager.get_room(room_code)

    if room is None:
        raise HTTPException(status_code=404, detail=ERR_ROOM_NOT_FOUND)

    return room.execute_command(request)
