from dataclasses import dataclass

from app.constants import DownlinkRate


@dataclass
class CommunicationsState:
    signal_strength_db: float = -70.0
    # link_status: str = 'Online'
    downlink_rate: DownlinkRate = DownlinkRate.MEDIUM

    def update_downlink_rate(self, downlink_rate: DownlinkRate) -> None:
        # if self.downlink_rate == downlink_rate:
        #     return
        self.downlink_rate = downlink_rate
