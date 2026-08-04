from dataclasses import dataclass, field

from app.managers.fault_manager import FaultManager


@dataclass
class PowerState:
    battery_percent: float = 100.0
    battery_voltage: float = 28.0
    #  power_generation_w
    #  power_consumption_w
    # solar_generation: float = 0
    # power_consumption: float = 0

    def update(self, dt: float, faults: FaultManager) -> None:
        pass

    def charge(self) -> None:
        pass

    def consume(self) -> None:
        pass
