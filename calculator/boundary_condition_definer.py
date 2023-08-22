from calculator.config import BoundaryConditionName, ConditionsInBuilding


class BoundaryConditionDefiner:
    @classmethod
    def define(cls, heat_information):
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
