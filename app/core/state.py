from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from app.constants import DownlinkRate, Mode
from app.models.fault import Fault


@dataclass
class MissionState:
    satellite_id: str

    # Position
    latitude: float = 0.0
    longitude: float = 0.0
    altitude_km: float = 550.0

    # Power
    battery_voltage: float = 28.0
    battery_percent: float = 100.0

    # Health
    temperature_c: float = 24.0
    signal_strength_db: float = -70.0

    # Mission configuration
    mode: Mode = Mode.NOMINAL
    downlink_rate: DownlinkRate = DownlinkRate.MEDIUM

    # Faults
    faults: list[Fault] = field(default_factory=list)

    # Time
    simulation_time: datetime = field(default_factory=lambda: datetime.now(UTC))
    last_updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def reset(self) -> None:
        """Restore spacecraft to nominal state."""
        self.mode = Mode.NOMINAL
        self.downlink_rate = DownlinkRate.MEDIUM

        self.battery_voltage = 28.0
        self.battery_percent = 100.0

        self.temperature_c = 24.0
        self.signal_strength_db = -70.0

        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude_km = 550.0

        self.faults.clear()

        now = datetime.now(UTC)
        self.simulation_time = now
        self.last_updated_at = now

    def update(self, delta_seconds: int = 1) -> None:
        """Advance the spacecraft simulation."""
        self.simulation_time += timedelta(seconds=delta_seconds)
        self.last_updated_at = datetime.now(UTC)

        # Future simulation logic:
        # - battery drain
        # - orbit propagation
        # - temperature changes
        # - signal strength changes
        # - apply active faults

    def set_mode(self, mode: Mode) -> None:
        self.mode = mode

    def set_downlink_rate(self, rate: DownlinkRate) -> None:
        self.downlink_rate = rate

    def inject_fault(self, fault: Fault) -> None:
        if fault not in self.faults:
            self.faults.append(fault)

    def clear_faults(self) -> None:
        self.faults.clear()
