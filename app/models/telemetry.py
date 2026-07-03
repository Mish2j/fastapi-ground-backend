from pydantic import BaseModel

class Telemetry(BaseModel):
    timestamp: str
    satellite_id: str
    mode: str
    downlink_rate: str
    battery_voltage: float
    temperature_c: float
    signal_db: float
    latitude: float
    longitude: float
    faults: list[str]