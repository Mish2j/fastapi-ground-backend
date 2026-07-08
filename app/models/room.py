from pydantic import BaseModel, Field


class CreateRoomRequest(BaseModel):
    name: str = Field(default='Mission Room')
    max_users: int = Field(default=4, ge=1, le=8)


class JoinRoomRequest(BaseModel):
    display_name: str = Field(min_length=1, max_length=40)


class RoomResponse(BaseModel):
    room_code: str
    name: str
    max_users: int
    active_users: int
