from fastapi import APIRouter, HTTPException

from app.constants import ERR_ROOM_NOT_FOUND
from app.managers.room_manager import room_manager
from app.models.participant import ParticipantResponse, ParticipantRoleRequest

router = APIRouter(prefix='/rooms', tags=['Participants'])


@router.get('/{room_code}/participants', response_model=list[ParticipantResponse])
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


@router.patch(
    '/{room_code}/participants/{participant_id}/role',
    response_model=ParticipantResponse,
)
def update_participant_role(
    room_code: str, participant_id: str, request: ParticipantRoleRequest
) -> ParticipantResponse:
    room = room_manager.get_room(room_code)

    if room is None:
        raise HTTPException(status_code=404, detail=ERR_ROOM_NOT_FOUND)

    try:
        participant = room.assign_role(
            request.requester_id, participant_id, request.role
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return ParticipantResponse(
        participant_id=participant.participant_id,
        display_name=participant.display_name,
        role=participant.role,
        is_connected=participant.is_connected,
        joined_at=participant.joined_at,
    )
