from calculator.config import BoundaryConditionName, ConditionsInBuilding


class BoundaryConditionDefiner:
    @classmethod
    def define(cls, heat_information):
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

        inside_boundary_condition = cls.inside(heat_information)

        outside_boundary_condition = cls.outside(heat_information)

        return {
            BoundaryConditionName.inside.value: inside_boundary_condition,
            BoundaryConditionName.outside.value: outside_boundary_condition
        }

    @staticmethod
    def inside(heat_information):
        inside_temperature = heat_information[ConditionsInBuilding.inside_temperature.value]
        inside_heater_power = heat_information[ConditionsInBuilding.inside_heater_power.value]

        if inside_temperature is not None:
            bc = BoundaryConditionName.dirichlet.value
        elif inside_heater_power is not None:
            bc = BoundaryConditionName.neumann.value
        else:
            bc = None
        return bc

    @staticmethod
    def outside(heat_information):
        outside_temperature = heat_information[ConditionsInBuilding.outside_temperature.value]
        outside_heater_power = heat_information[ConditionsInBuilding.outside_heater_power.value]

        if outside_temperature is not None:
            bc = BoundaryConditionName.dirichlet.value
        elif outside_heater_power is not None:
            bc = BoundaryConditionName.neumann.value
        else:
            bc = None
        return bc
