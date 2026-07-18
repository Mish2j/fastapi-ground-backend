from dataclasses import dataclass, field
from datetime import datetime, timezone
import random
import asyncio
from fastapi import WebSocket

from app.constants import DownlinkRate, Mode, ParticipantRole, Status, Command, Event
from app.core.participant import Participant
from app.models.command import (
    CommandRequest,
    SetModeParams,
    SetDownlinkRateParams,
    InjectFaultParams,
)

MAX_TELEMETRY_HISTORY = 500
MAX_EVENT_LOG = 200


# TODO: add room cleanup
@dataclass
class MissionRoom:
    room_code: str
    name: str
    max_users: int
    is_streaming: bool = False
    stream_task: asyncio.Task | None = None
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    satellite_state: dict = field(
        default_factory=lambda: {
            'satellite_id': 'SAT-001',
            'mode': Mode.NOMINAL,
            'downlink_rate': DownlinkRate.LOW,
            'faults': [],
        }
    )
    telemetry_history: list[dict] = field(default_factory=list)
    event_log: list[dict] = field(default_factory=list)
    participants: dict[str, Participant] = field(default_factory=dict)
    connections: list[WebSocket] = field(default_factory=list)

    def active_users(self) -> int:
        return len(self.participants)

    def join(self, display_name: str) -> Participant:
        if self.active_users() >= self.max_users:
            raise ValueError('Room is full')

        participant = Participant(display_name=display_name)

        # first person = FLIGHT_DIRECTOR
        if self.active_users() == 0:
            participant.update_role(ParticipantRole.FLIGHT_DIRECTOR)

        participant.connect()

        self.participants[participant.participant_id] = participant

        return participant

    def save_telemetry(self, telemetry: dict):
        if len(self.telemetry_history) > MAX_TELEMETRY_HISTORY:
            self.telemetry_history.pop(0)

        self.telemetry_history.append(telemetry)

    def get_latest_telemetry(self) -> dict:
        if not self.telemetry_history:
            # May want to generate and return telemetry instead: return self.generate_telemetry()
            return None

        return self.telemetry_history[-1]

    def get_telemetry_history(self, limit: int = 100) -> dict:
        return self.telemetry_history[-limit:]

    def generate_telemetry(self) -> dict:
        telemetry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'satellite_id': self.satellite_state['satellite_id'],
            'mode': self.satellite_state['mode'],
            'downlink_rate': self.satellite_state['downlink_rate'],
            'battery_voltage': round(random.uniform(27.5, 29.0), 2),
            'temperature_c': round(random.uniform(18.0, 32.0), 2),
            'signal_db': round(random.uniform(-90, -60), 2),
            'latitude': round(random.uniform(-60, 60), 4),
            'longitude': round(random.uniform(-180, 180), 4),
            'faults': self.satellite_state['faults'],
        }

        self.save_telemetry(telemetry)

        return telemetry

    def save_event(self, event: dict):
        if len(self.event_log) > MAX_EVENT_LOG:
            self.event_log.pop(0)

        self.event_log.append(event)

    def add_event(
        self,
        event_type: str,
        message: str,
        status: str = 'INFO',
        command: str | None = None,
    ) -> dict:
        event = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'type': event_type,
            'status': status,
            'message': message,
            'command': command,
        }

        self.save_event(event)

        return event

    def get_events(self, limit: int = 50) -> list[dict]:
        return self.event_log[-limit:]

    def execute_command(self, request: CommandRequest) -> dict:
        # command = request.command
        # result = ex_cmd(request)

        # add_event(
        #     event_type=Event.COMMAND,
        #     command=command,
        #     status=result['status'],
        #     message=result['message'],
        # )

        # return result

        command = request.command
        params = request.params

        if command == Command.SET_MODE:
            result = self.__set_mode(params)

        elif command == Command.SET_DOWNLINK_RATE:
            result = self.__set_downlink_rate(params)

        elif command == Command.INJECT_FAULT:
            result = self.__inject_fault(params)

        elif command == Command.CLEAR_FAULTS:
            result = self.__clear_faults()

        else:
            result = {
                'status': Status.REJECTED,
                'message': f'Unknown command: {command}',
            }

        self.add_event(
            event_type=Event.COMMAND,
            command=command,
            status=result['status'],
            message=result['message'],
        )

        return result

    def __set_mode(self, params: dict) -> dict:
        try:
            validated = SetModeParams(**params)
        except Exception as error:
            return {
                'status': Status.REJECTED,
                'message': str(error),
            }

        self.satellite_state['mode'] = validated.mode

        return {
            'status': Status.ACCEPTED,
            'message': f'Mode changed to {validated.mode}',
        }

    def __set_downlink_rate(self, params: dict) -> dict:
        try:
            validated = SetDownlinkRateParams(**params)
        except Exception as error:
            return {
                'status': Status.REJECTED,
                'message': str(error),
            }

        self.satellite_state['downlink_rate'] = validated.rate

        return {
            'status': Status.ACCEPTED,
            'message': f'Downlink rate changed to {validated.rate}',
        }

    def __inject_fault(self, params: dict) -> dict:
        try:
            validated = InjectFaultParams(**params)
        except Exception as error:
            return {
                'status': Status.REJECTED,
                'message': str(error),
            }

        if validated.fault not in self.satellite_state['faults']:
            self.satellite_state['faults'].append(validated.fault)

        return {
            'status': Status.ACCEPTED,
            'message': f'Fault injected: {validated.fault}',
        }

    def __clear_faults(self) -> dict:
        self.satellite_state['faults'].clear()

        return {
            'status': Status.ACCEPTED,
            'message': 'All faults cleared',
        }

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections.append(websocket)
        print(f'Client connected: {websocket.client.host}:{websocket.client.port}')

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.connections:
            self.connections.remove(websocket)
            print(
                f'Client disconnected: {websocket.client.host}:{websocket.client.port}'
            )

    async def broadcast_telemetry(self, telemetry: dict) -> None:
        disconnected = []

        for connection in self.connections:
            try:
                await connection.send_json(telemetry)
            except Exception:
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)

    async def start_stream(self) -> None:

        if self.is_streaming:
            return

        self.is_streaming = True
        self.stream_task = asyncio.create_task(self.__telemetry_loop())

    async def stop_stream(self) -> None:
        if not self.is_streaming:
            return

        self.is_streaming = False

        if self.stream_task is not None:
            self.stream_task.cancel()
            self.stream_task = None

    async def __telemetry_loop(self) -> None:
        try:
            while self.is_streaming:
                telemetry = self.generate_telemetry()

                # send to ALL connections
                await self.broadcast_telemetry(telemetry)

                # wait 1 second, repeat
                await asyncio.sleep(1)

        except asyncio.CancelledError:
            pass
