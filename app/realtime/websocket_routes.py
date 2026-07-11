import asyncio

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

    try:
        while True:
            telemetry = room.generate_telemetry()
            await room.broadcast_telemetry(telemetry)
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        room.disconnect(websocket)

    # Use connection_manager instead?
    # await manager.connect(websocket)

    # try:
    #     while True:
    #         telemetry = create_new_telemetry()
    #         await manager.send_json(websocket, telemetry)
    #         await asyncio.sleep(1)

    # except WebSocketDisconnect:
    #     manager.disconnect(websocket)
    #     print('Client disconnected')
