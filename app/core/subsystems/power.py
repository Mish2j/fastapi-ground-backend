from dataclasses import dataclass

from app.constants import FaultType
from app.core.subsystems.faults.fault_manager import FaultManager


@dataclass
class PowerState:
    battery_percent: float = 100.0
    battery_voltage: float = 28.0
    #  power_generation_w
    #  power_consumption_w
    # solar_generation: float = 0
    # power_consumption: float = 0

    def update(self, delta_seconds: float, faults: FaultManager) -> None:
        drain_rate = 0.001

        if faults.has(FaultType.BATTERY_DEGRADATION):
            drain_rate *= 5

        self.battery_percent = max(
            0.0, self.battery_percent - drain_rate * delta_seconds
        )

    def charge(self) -> None:
        pass

    def consume(self) -> None:
        pass
