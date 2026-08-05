from datetime import datetime

from pydantic import BaseModel

from app.constants import DownlinkRate, Mode
from app.models.fault import Fault


class Telemetry(BaseModel):
    timestamp: datetime
    satellite_id: str
    mode: Mode
    downlink_rate: DownlinkRate
    battery_percent: float
    battery_voltage: float
    temperature_c: float
    signal_strength_db: float
    latitude: float
    longitude: float
    altitude_km: float
    faults: list[Fault]
