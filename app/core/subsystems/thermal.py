from dataclasses import dataclass, field

from app.core.subsystems.power import PowerState
from app.managers.fault_manager import FaultManager


@dataclass
class ThermalState:
    temperature_c: float = 24.0
    # heater_enabled: bool = False

    def update(
        self,
        dt: float,
        power: PowerState,
        faults: FaultManager,
    ) -> None:
        pass
