from dataclasses import dataclass, field

from app.constants import Mode


@dataclass
class ComputerState:
    mode: Mode = Mode.NOMINAL
    # uptime
    # boot_state
