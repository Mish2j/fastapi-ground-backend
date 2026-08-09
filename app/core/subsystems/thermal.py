from dataclasses import dataclass, field

from app.core.faults.fault_manager import FaultManager
from app.core.subsystems.power import PowerState


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
