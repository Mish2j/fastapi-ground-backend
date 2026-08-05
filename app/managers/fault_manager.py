from dataclasses import dataclass, field

from app.models.fault import Fault


@dataclass
class FaultManager:
    active_faults: list[Fault] = field(default_factory=list)

    def update(self, dt) -> None:
        pass

    def inject_fault(self, fault: Fault) -> None:
        if fault not in self.active_faults:
            self.active_faults.append(fault)

    def clear_active_faults(self) -> None:
        self.active_faults.clear()
