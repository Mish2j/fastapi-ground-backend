from fastapi import APIRouter, WebSocket, WebSocketDisconnect

# from app.realtime.connection_manager import manager

# from app.services.telemetry_service import create_new_telemetry
from app.services.room_service import room_manager

router = APIRouter(prefix='/ws/rooms/{room_code}', tags=['Websocket'])


@router.websocket('/telemetry')
async def telemetry_websocket(websocket: WebSocket, room_code: str):
    room = room_manager.get_room(room_code)

    if room is None:
        await websocket.close(code=1008)
        return

    await room.connect(websocket)
    await room.start_stream()

    try:
        while True:
            # wait for messages from the client & detect disconnection.
            await websocket.receive_text()

    except WebSocketDisconnect:
        room.disconnect(websocket)

    if not room.connections:
        # Stop stream if no one is left in the room
        await room.stop_stream()
