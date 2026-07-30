from dataclasses import dataclass, field

from fastapi import WebSocket, WebSocketDisconnect

from app.models.telemetry import Telemetry


@dataclass
class WebSocketManager:
    connections: dict[str, dict[str, WebSocket]] = field(default_factory=dict)

    async def connect(
        self, room_code: str, participant_id: str, websocket: WebSocket
    ) -> None:
        await websocket.accept()

        if room_code not in self.connections:
            self.connections[room_code] = {}

        self.connections[room_code][participant_id] = websocket

        if websocket.client:
            print(f'Client connected: {websocket.client.host}:{websocket.client.port}')

    def disconnect(
        self, room_code: str, participant_id: str, websocket: WebSocket
    ) -> None:
        room_connections = self.connections.get(room_code)

        if room_connections is None:
            return

        room_connections.pop(participant_id, None)

        if websocket.client:
            print(
                f'Client disconnected: {websocket.client.host}:{websocket.client.port}'
            )

        if not room_connections:
            self.connections.pop(room_code, None)

    async def broadcast(self, room_code: str, data: Telemetry | dict) -> None:
        room_connections = self.connections.get(room_code)

        if room_connections is None:
            return

        disconnected = []

        for participant_id, websocket in room_connections.items():
            try:
                await websocket.send_json(data)

            except WebSocketDisconnect:
                disconnected.append(participant_id)

        for participant_id in disconnected:
            websocket = room_connections[participant_id]
            self.disconnect(room_code, participant_id, websocket)


websocket_manager = WebSocketManager()
