from dataclasses import dataclass, field

from app.constants import DownlinkRate


@dataclass
class CommunicationsState:
    signal_strength_db: float = -70.0
    # link_status: str = 'Online'
    downlink_rate: DownlinkRate = DownlinkRate.MEDIUM

    def update(self, dt: float) -> None:
        pass
