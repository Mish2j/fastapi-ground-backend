from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.managers.room_manager import room_manager
from app.managers.websocket_manager import websocket_manager
from app.services.telemetry_service import telemetry_service

router = APIRouter(
    prefix='/ws/rooms/{room_code}/participants/{participant_id}', tags=['Websocket']
)


@router.websocket('/telemetry')
async def telemetry_websocket(
    websocket: WebSocket, room_code: str, participant_id: str
):
    room = room_manager.get_room(room_code)

    if room is None:
        await websocket.close(code=1008)
        return

    participant = room.get_participant(participant_id)

    if participant is None:
        await websocket.close(code=1008)
        return

    participant.connect()

    await websocket_manager.connect(
        room_code,
        participant_id,
        websocket,
    )

    await telemetry_service.start_stream(room)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        room.disconnect_participant(participant_id)

    finally:
        participant.disconnect()
        websocket_manager.disconnect(room_code, participant_id, websocket)
        room.touch()

        if not room.has_connected_users():
            await telemetry_service.stop_stream(room_code)
