import logging
import sys
from dataclasses import dataclass

from calculator.config import GLOBAL_LOGGING_LEVEL

logging.basicConfig(stream=sys.stdout, level=GLOBAL_LOGGING_LEVEL)


@dataclass
class OutsideInsideThermalData:
    OUTSIDE_TEMPERATURE: float
    INSIDE_HEATER_POWER: float = None
    INSIDE_TEMPERATURE: float = None
    OUTSIDE_HEATER_POWER: float = None

    def validated_data_presence(self):
        if self.OUTSIDE_TEMPERATURE is None:
            logging.error("Outside temperature is not defined.")
            raise ValueError("Outside temperature must be defined")
