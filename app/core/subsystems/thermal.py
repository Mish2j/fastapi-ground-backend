from dataclasses import dataclass

from app.core.faults.fault_manager import FaultManager
from app.core.faults.fault_types import FaultType
from app.core.subsystems.power import PowerState


@dataclass
class ThermalState:
    # TODO: current rates are very slow

    # below this temperature, the spacecraft is considered too cold
    TEMPERATURE_LOW_C = 0.0

    # nominal temperature for the spacecraft
    TEMPERATURE_NOMINAL_C = 24.0

    # above this temperature, the spacecraft is considered too hot
    TEMPERATURE_HIGH_C = 50.0

    # rate at which the spacecraft cools down when heater is off
    TEMPERATURE_COOLING_RATE = 0.002

    # rate at which the spacecraft heats up when heater is on
    TEMPERATURE_HEATING_RATE = 0.003

    # multiplier for temperature drain rate when thermal degradation fault is active
    TEMPERATURE_DEGRADATION_MULTIPLIER = 2

    temperature_c: float = TEMPERATURE_NOMINAL_C
    # heater_enabled: bool = False

    @property
    def is_high(self) -> bool:
        return self.temperature_c >= self.TEMPERATURE_HIGH_C

    @property
    def is_low(self) -> bool:
        return self.temperature_c <= self.TEMPERATURE_LOW_C

    def update(
        self,
        delta_seconds: float,
        power: PowerState,
        faults: FaultManager,
    ) -> None:
        if faults.has(FaultType.HIGH_TEMPERATURE):
            self.temperature_c += (
                self.TEMPERATURE_HEATING_RATE
                * self.TEMPERATURE_DEGRADATION_MULTIPLIER
                * delta_seconds
            )
            return

        # TODO: if faults.has(FaultType.LOW_TEMPERATURE):

        if self.temperature_c > self.TEMPERATURE_NOMINAL_C:
            self.temperature_c = max(
                self.TEMPERATURE_NOMINAL_C,
                self.temperature_c - self.TEMPERATURE_COOLING_RATE * delta_seconds,
            )
        elif self.temperature_c < self.TEMPERATURE_NOMINAL_C:
            self.temperature_c = min(
                self.TEMPERATURE_NOMINAL_C,
                self.temperature_c + self.TEMPERATURE_HEATING_RATE * delta_seconds,
            )
