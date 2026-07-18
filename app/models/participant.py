from pydantic import BaseModel

from app.constants import ParticipantRole


class ParticipantResponse(BaseModel):
    participant_id: str
    display_name: str
    role: ParticipantRole
    is_connected: bool
    joined_at: str
