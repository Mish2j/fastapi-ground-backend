from dataclasses import dataclass

from app.core.faults.fault_manager import FaultManager
from app.core.faults.fault_types import FaultType


@dataclass
class PowerState:
    battery_percent: float = 100.0
    battery_voltage: float = 28.0
    #  power_generation_w
    #  power_consumption_w
    # solar_generation: float = 0
    # power_consumption: float = 0

    NOMINAL_DRAIN_RATE = 0.001
    BATTERY_DEGRADATION_MULTIPLIER = 5
    LOW_BATTERY_THRESHOLD = 20

    @property
    def is_low(self) -> bool:
        return self.battery_percent < self.LOW_BATTERY_THRESHOLD

    def update(self, delta_seconds: float, faults: FaultManager) -> None:
        drain_rate = self.NOMINAL_DRAIN_RATE

        if faults.has(FaultType.BATTERY_DEGRADATION):
            drain_rate *= self.BATTERY_DEGRADATION_MULTIPLIER

        self.battery_percent = max(
            0.0, self.battery_percent - drain_rate * delta_seconds
        )

        # bettery voltage drops as battery percentage drops. It slowly decreases from 28V to 24V as battery percentage goes from 100% to 0%
        self.battery_voltage = 24.0 + (self.battery_percent / 100) * 4.0

    def charge(self) -> None:
        pass

    def consume(self) -> None:
        pass
