import math
from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.core.subsystems.orbit.orbit import OrbitState
from app.core.subsystems.orbit.orbit_provider import OrbitProvider


@dataclass
class SimpleOrbitProvider(OrbitProvider):
    # Low Earth Orbit (LEO) by default

    altitude_km: float = 550.0
    orbital_period_minutes: float = 90.0
    inclination_deg: float = 51.6
    epoch: datetime | None = None

    def calculate(
        self,
        simulation_time: datetime,
    ) -> OrbitState:
        """
        Calculates the satellite's position in orbit at a given simulation time.
        Returns latitude, longitude, and altitude based on a simplified circular orbit model.
        """

        if self.epoch is None:
            self.epoch = datetime.now(UTC)

        # ensure simulation_time is timezone-aware
        if simulation_time.tzinfo is None:
            simulation_time = simulation_time.replace(tzinfo=UTC)

        # How much time has passed?
        elapsed_seconds = (simulation_time - self.epoch).total_seconds()

        # Where in the orbit are we?
        orbital_position_deg = (
            elapsed_seconds / (self.orbital_period_minutes * 60) * 360
        )

        # reset back to 0deg
        orbital_position_deg %= 360

        latitude = self.inclination_deg * math.sin(math.radians(orbital_position_deg))

        longitude = orbital_position_deg - 180

        return OrbitState(
            latitude=latitude,
            longitude=longitude,
            altitude_km=self.altitude_km,
            velocity_km_s=7.6,
            last_updated_at=datetime.now(UTC),
        )
