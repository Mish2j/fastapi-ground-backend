import asyncio
from dataclasses import dataclass, field

from app.core.room import MissionRoom
from app.core.state import MissionState
from app.managers.websocket_manager import websocket_manager
from app.models.telemetry import Telemetry


@dataclass
class TelemetryService:
    stream_tasks: dict[str, asyncio.Task] = field(default_factory=dict)

    def generate(self, mission_state: MissionState) -> Telemetry:

        return Telemetry(
            timestamp=mission_state.simulation_time,
            satellite_id=mission_state.satellite_id,
            mode=mission_state.mode,
            downlink_rate=mission_state.downlink_rate,
            battery_voltage=mission_state.battery_voltage,
            temperature_c=mission_state.temperature_c,
            signal_strength_db=mission_state.signal_strength_db,
            latitude=mission_state.latitude,
            longitude=mission_state.longitude,
            altitude_km=mission_state.altitude_km,
            faults=mission_state.faults,
        )

    async def start_stream(self, room: MissionRoom) -> None:
        room_code = room.room_code

        if room_code in self.stream_tasks:
            return

        self.stream_tasks[room_code] = asyncio.create_task(self.__telemetry_loop(room))

    async def stop_stream(self, room_code: str) -> None:
        task = self.stream_tasks.pop(room_code, None)

        if task:
            task.cancel()

    def is_streaming(self, room_code: str) -> bool:
        return room_code in self.stream_tasks

    async def __telemetry_loop(self, room: MissionRoom) -> None:
        try:
            while True:
                room.mission_state.update()

                telemetry = self.generate(room.mission_state)

                room.save_telemetry(telemetry)

                # send to ALL connections
                await websocket_manager.broadcast(room.room_code, telemetry)
                # wait 1 second, repeat
                await asyncio.sleep(1)

        except asyncio.CancelledError:
            pass


telemetry_service = TelemetryService()
