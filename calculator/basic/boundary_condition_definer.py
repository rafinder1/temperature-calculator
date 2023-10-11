import logging

from calculator.basic.config import ConditionsInBuilding
from enum import Enum


class BoundaryConditionDefiner(Enum):
    Neumann = "neumann"
    Dirichlet = "dirichlet"
    InsideBC = "inside_boundary_condition"
    OutsideBC = "outside_boundary_condition"

    @classmethod
    def define(cls, heat_information: dict) -> dict:
        """
        Boundary conditions occurring in the building partition are being defined. This process determines two types of
        boundary conditions: those occurring inside the building and those pertaining to the external environment.
        This method relies on input data provided in the form of a dictionary, which contains information regarding
        temperature and/or heat transfer. Within this method, two types of boundary conditions are possible:

        1. Dirichlet Boundary Condition - This type of boundary condition relates to temperature. A temperature value
        in degrees Celsius is passed as part of the input dictionary.

        2. Neumann Boundary Condition - In this case, heat transfer is conveyed in units of W/m² * °C as part of
        the input dictionary.

        This method returns a dictionary with two keys. The first key pertains to interior partition conditions,
        and the second key relates to conditions of the external environment. Through this process, it becomes possible
        to precisely determine how thermal energy passes through the building partition based on the provided data.

        :param heat_information: A dictionary containing information about temperature and/or heat transfer.
        :return: A dictionary with keys BoundaryConditionName.inside and BoundaryConditionName.outside.
        """
        logging.info(f"Determining the conditions in the partition based on data: {heat_information}")

        inside_boundary_condition = cls.inside(heat_information)
        logging.info(f"Inside exist condition: {inside_boundary_condition}")

        outside_boundary_condition = cls.outside(heat_information)
        logging.info(f"Outside exist condition: {outside_boundary_condition}")

        return {
            cls.InsideBC.value: inside_boundary_condition,
            cls.OutsideBC.value: outside_boundary_condition
        }

    @classmethod
    def define_dirichlet_or_neumann(cls, temperature: float, heater_power: float) -> str:
        if temperature is not None:
            return cls.Dirichlet.value
        elif heater_power is not None:
            return cls.Neumann.value
        else:
            raise ValueError("You need to define the temperature or power of the radiator")

    @classmethod
    def inside(cls, heat_information: dict) -> str:
        inside_temperature = heat_information[ConditionsInBuilding.inside_temperature.value]
        inside_heater_power = heat_information[ConditionsInBuilding.inside_heater_power.value]

        return cls.define_dirichlet_or_neumann(temperature=inside_temperature, heater_power=inside_heater_power)

    @classmethod
    def outside(cls, heat_information: dict) -> str:
        outside_temperature = heat_information[ConditionsInBuilding.outside_temperature.value]
        outside_heater_power = heat_information[ConditionsInBuilding.outside_heater_power.value]

        return cls.define_dirichlet_or_neumann(temperature=outside_temperature, heater_power=outside_heater_power)
