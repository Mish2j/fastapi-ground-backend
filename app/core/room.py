from dataclasses import dataclass, field
from datetime import datetime, timezone
import random
from fastapi import WebSocket

from app.constants import DownlinkRate, Mode, Status, Command, Event
from app.models.command import (
    CommandRequest,
    SetModeParams,
    SetDownlinkRateParams,
    InjectFaultParams,
)

MAX_TELEMETRY_HISTORY = 500
MAX_EVENT_LOG = 200


@dataclass
class MissionRoom:
    room_code: str
    name: str
    max_users: int
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
    participants: dict[str, str] = field(default_factory=dict)
    connections: list[WebSocket] = field(default_factory=list)

    def active_users(self) -> int:
        return len(self.participants)

    def join(self, participant_id: str, display_name: str) -> None:
        if self.active_users() >= self.max_users:
            raise ValueError('Room is full')

        self.participants[participant_id] = display_name

    def save_telemetry(self, telemetry: dict):
        if len(self.telemetry_history) > MAX_TELEMETRY_HISTORY:
            self.telemetry_history.pop(0)

        self.telemetry_history.append(telemetry)

    def get_latest_telemetry(self) -> dict:
        if not self.telemetry_history:
            return None

            # May want to generate and return telemetry instead
            # return self.generate_telemetry()

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
            result = self._set_mode(params)

        elif command == Command.SET_DOWNLINK_RATE:
            result = self._set_downlink_rate(params)

        elif command == Command.INJECT_FAULT:
            result = self._inject_fault(params)

        elif command == Command.CLEAR_FAULTS:
            result = self._clear_faults()

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

    def _set_mode(self, params: dict) -> dict:
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

    def _set_downlink_rate(self, params: dict) -> dict:
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

    def _inject_fault(self, params: dict) -> dict:
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

    def _clear_faults(self) -> dict:
        self.satellite_state['faults'].clear()

        return {
            'status': Status.ACCEPTED,
            'message': 'All faults cleared',
        }

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def broadcast_telemetry(self, telemetry: dict) -> None:
        disconnected = []

        for connection in self.connections:
            try:
                await connection.send_json(telemetry)
            except Exception:
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)
