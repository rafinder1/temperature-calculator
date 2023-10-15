import logging
from dataclasses import dataclass

logging.basicConfig(stream=sys.stdout, level=GLOBAL_LOGGING_LEVEL)


@dataclass
class OutsideInsideThermalData:
    OUTSIDE_TEMPERATURE: float
    INSIDE_HEATER_POWER: float
    INSIDE_TEMPERATURE: float = None
    OUTSIDE_HEATER_POWER: float = None

    def validated_data_presence(self):
        if self.OUTSIDE_TEMPERATURE is None:
            logging.error("Outside temperature is not defined.")
            raise ValueError("Outside temperature must be defined")
        if self.INSIDE_HEATER_POWER is None:
            logging.error("Inside heater power is not defined.")
            raise ValueError("Inside heater power must be defined")
