import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.realtime.connection_manager import manager
from app.services.telemetry_service import create_new_telemetry


router = APIRouter(prefix="ws", tags=["Websocket"])


@router.websocket("/telemetry")
async def telemetry_websocket(websocket: WebSocket):
    await manager.connect(websocket)

    try: 
        while True:
            telemetry = create_new_telemetry()
            await manager.send_json(websocket, telemetry)
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")