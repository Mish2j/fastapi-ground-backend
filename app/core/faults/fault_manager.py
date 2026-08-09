from dataclasses import dataclass, field

from app.core.faults.fault import Fault
from app.core.faults.fault_types import FaultType


@dataclass
class FaultManager:
    active_faults: list[Fault] = field(default_factory=list)

    def update(self, delta_seconds: float) -> None:
        pass

    def inject(self, fault: Fault) -> None:
        if fault not in self.active_faults:
            self.active_faults.append(fault)

    def clear_all_faults(self) -> None:
        self.active_faults.clear()

    def clear_fault(self, fault_type: FaultType) -> None:
        self.active_faults = [
            fault for fault in self.active_faults if fault.type != fault_type
        ]

    def has(self, fault_type: FaultType) -> bool:
        return any(
            fault.type == fault_type and fault.active for fault in self.active_faults
        )
