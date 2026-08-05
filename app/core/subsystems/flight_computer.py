from dataclasses import dataclass, field

from app.constants import Mode


@dataclass
class FlightComputerState:
    mode: Mode = Mode.NOMINAL
    # uptime
    # boot_state

    def update_mode(self, new_mode: Mode) -> None:

        self.mode = new_mode
