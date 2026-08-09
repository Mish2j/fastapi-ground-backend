import asyncio
from dataclasses import dataclass, field

from app.constants import SIMULATION_STEP_SECONDS
from app.core.mission_state import MissionState
from app.core.room import MissionRoom
from app.core.subsystems.orbit.orbit_provider import OrbitProvider
from app.core.subsystems.orbit.simple_orbit_provider import SimpleOrbitProvider
from app.managers.websocket_manager import websocket_manager
from app.models.telemetry import Telemetry
from app.services.event_service import event_service


@dataclass
class TelemetryService:
    orbit_provider: OrbitProvider
    stream_tasks: dict[str, asyncio.Task] = field(default_factory=dict)

    def generate(self, mission_state: MissionState) -> Telemetry:

        return Telemetry(
            timestamp=mission_state.simulation_time,
            satellite_id=mission_state.satellite_id,
            mode=mission_state.computer.mode,
            downlink_rate=mission_state.communications.downlink_rate,
            battery_percent=mission_state.power.battery_percent,
            battery_voltage=mission_state.power.battery_voltage,
            temperature_c=mission_state.thermal.temperature_c,
            signal_strength_db=mission_state.communications.signal_strength_db,
            latitude=mission_state.orbit.latitude,
            longitude=mission_state.orbit.longitude,
            altitude_km=mission_state.orbit.altitude_km,
            faults=mission_state.faults.active_faults,
        )

    async def start_stream(self, room: MissionRoom) -> None:
        print('Starting stream')
        room_code = room.room_code

        if room_code in self.stream_tasks:
            return

        self.stream_tasks[room_code] = asyncio.create_task(self.__telemetry_loop(room))
        print('stream_tasks: ', self.stream_tasks)

    async def stop_stream(self, room_code: str) -> None:
        task = self.stream_tasks.pop(room_code, None)

        if task:
            task.cancel()

    def is_streaming(self, room_code: str) -> bool:
        return room_code in self.stream_tasks

    async def __telemetry_loop(self, room: MissionRoom) -> None:
        print('Telemetry loop started')
        try:
            while True:
                print('tick')
                room.mission_state.update(
                    self.orbit_provider,
                    delta_seconds=SIMULATION_STEP_SECONDS,
                )

                event_service.collect_events(
                    mission_state=room.mission_state,
                    room=room,
                )

                telemetry = self.generate(room.mission_state)

                room.save_telemetry(telemetry)

                # send to ALL connections
                print('Broadcasting...')
                await websocket_manager.broadcast(
                    room.room_code,
                    telemetry.model_dump(mode='json'),
                )
                print('Broadcast finished')
                # wait x second, repeat
                await asyncio.sleep(SIMULATION_STEP_SECONDS)

        except asyncio.CancelledError:
            print('Telemetry loop cancelled')


telemetry_service = TelemetryService(
    orbit_provider=SimpleOrbitProvider(),
)
