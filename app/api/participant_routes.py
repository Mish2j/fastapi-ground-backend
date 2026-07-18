from fastapi import APIRouter, HTTPException

from app.constants import ERR_ROOM_NOT_FOUND
from app.models.participant import ParticipantResponse
from app.services.room_service import room_manager

router = APIRouter(prefix='/rooms', tags=['Participants'])


@router.get('/rooms/{room_code}/participants', response_model=list[ParticipantResponse])
def get_room_participants(room_code: str) -> list[ParticipantResponse]:
    room = room_manager.get_room(room_code)

    if room is None:
        raise HTTPException(status_code=404, detail=ERR_ROOM_NOT_FOUND)

    return [
        ParticipantResponse(
            participant_id=participant.participant_id,
            display_name=participant.display_name,
            role=participant.role,
            is_connected=participant.is_connected,
            joined_at=participant.joined_at,
        )
        for participant in room.participants.values()
    ]
