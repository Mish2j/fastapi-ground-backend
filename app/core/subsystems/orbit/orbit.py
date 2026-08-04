from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class OrbitState:
    latitude: float = 0.0
    longitude: float = 0.0
    altitude_km: float = 550.0
    velocity_km_s: float = 7.6

    last_updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
