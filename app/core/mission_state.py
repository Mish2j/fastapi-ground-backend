from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from app.constants import DownlinkRate, Mode
from app.core.events.event import Event

# from app.core.subsystems.attitude import AttitudeState
from app.core.events.event_types import EventStatus, EventType
from app.core.faults.fault import Fault
from app.core.faults.fault_manager import FaultManager
from app.core.subsystems.communications import CommunicationsState
from app.core.subsystems.flight_computer import FlightComputerState
from app.core.subsystems.orbit.orbit import OrbitState

# from app.core.subsystems.payload import PayloadState
from app.core.subsystems.orbit.orbit_provider import OrbitProvider
from app.core.subsystems.power import PowerState
from app.core.subsystems.thermal import ThermalState


@dataclass
class MissionState:
    satellite_id: str = 'SAT-001'

    pending_events: list[Event] = field(default_factory=list)

    power: PowerState = field(default_factory=PowerState)
    thermal: ThermalState = field(default_factory=ThermalState)
    communications: CommunicationsState = field(default_factory=CommunicationsState)
    orbit: OrbitState = field(default_factory=OrbitState)
    # attitude: AttitudeState = field(default_factory=AttitudeState)
    # payload: PayloadState = field(default_factory=PayloadState)
    computer: FlightComputerState = field(default_factory=FlightComputerState)
    faults: FaultManager = field(default_factory=FaultManager)

    # Time
    simulation_time: datetime = field(default_factory=lambda: datetime.now(UTC))
    last_updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def reset(self) -> None:
        """Restore spacecraft to nominal state."""

        # now = datetime.now(UTC)
        # self.simulation_time = now
        # self.last_updated_at = now

    def update(self, orbit_provider: OrbitProvider, delta_seconds: float = 1.0) -> None:
        self.simulation_time += timedelta(seconds=delta_seconds)

        self.faults.update(delta_seconds)

        self.power.update(delta_seconds, self.faults)
        self.thermal.update(delta_seconds, self.power, self.faults)
        self.orbit = orbit_provider.calculate(self.simulation_time)
        # self.communications.update(self, delta_seconds)
        # self.payload.update(self, delta_seconds)
        # self.attitude.update(self, delta_seconds)
        # self.computer.update(delta_seconds, self.power)

        self.__check_safe_mode()

        self.last_updated_at = datetime.now(UTC)

    def set_mode(self, mode: Mode) -> None:
        self.computer.update_mode(mode)

    def set_downlink_rate(self, rate: DownlinkRate) -> None:
        self.communications.update_downlink_rate(rate)

    def inject_fault(self, fault: Fault) -> None:
        self.faults.inject(fault)

    def clear_faults(self) -> None:
        self.faults.clear_all_faults()

    def __check_safe_mode(self) -> None:
        if self.power.is_low:
            self.__enter_safe_mode()

    def __enter_safe_mode(self) -> None:
        self.computer.update_mode(Mode.SAFE)

        self.communications.update_downlink_rate(DownlinkRate.LOW)

        event = Event(
            timestamp=datetime.now(UTC),
            type=EventType.MODE_CHANGE,
            status=EventStatus.INFO,
            message='Spacecraft has entered SAFE mode due to low power.',
        )

        self.pending_events.append(event)

        # TODO:
        # SAFE mode:
        # - disable payload
        # - reduce power consumption
        # - change telemetry frequency
        # - disable experiments
        # - enable beacon mode
