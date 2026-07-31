from fastapi import APIRouter, HTTPException

from app.constants import ERR_PARTICIPANT_NOT_FOUND, ERR_ROOM_NOT_FOUND
from app.managers.room_manager import room_manager
from app.models.command import CommandRequest
from app.services.command_service import command_service

router = APIRouter(prefix='/rooms/{room_code}/commands', tags=['Commands'])


@router.post('')
def send_command(room_code: str, request: CommandRequest):
    room = room_manager.get_room(room_code)

    if room is None:
        raise HTTPException(status_code=404, detail=ERR_ROOM_NOT_FOUND)

    participant = room.get_participant(request.participant_id)

    if participant is None:
        raise HTTPException(
            status_code=404,
            detail=ERR_PARTICIPANT_NOT_FOUND,
        )

    return command_service.execute(
        room,
        participant,
        request,
    )
