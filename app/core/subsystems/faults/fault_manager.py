from dataclasses import dataclass, field

from app.constants import FaultType
from app.core.subsystems.faults.fault import Fault


@dataclass
class FaultManager:
    active_faults: list[Fault] = field(default_factory=list)

    def update(self, delta_seconds: float) -> None:
        pass

    def inject(self, fault: Fault) -> None:
        if fault not in self.active_faults:
            self.active_faults.append(fault)

    def clear(self) -> None:
        self.active_faults.clear()

    def has(self, fault_type: FaultType) -> bool:
        return any(
            fault.type == fault_type and fault.active for fault in self.active_faults
        )
