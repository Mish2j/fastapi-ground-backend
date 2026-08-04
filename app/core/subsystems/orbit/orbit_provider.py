from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from app.core.subsystems.orbit.orbit import OrbitState


@dataclass
class OrbitProvider(ABC):
    @abstractmethod
    def calculate(
        self,
        simulation_time: datetime,
    ) -> OrbitState:
        """Calculate spacecraft orbit for the given simulation time."""
        raise NotImplementedError
