from main.config import BoundaryConditionName


class BoundaryConditionDefiner:
    @classmethod
    def define(cls, heat_information):
        inside_boundary_condition = cls.inside(heat_information)

        outside_boundary_condition = cls.outside(heat_information)

        return {
            "inside_boundary_condition": inside_boundary_condition,
            "outside_boundary_condition": outside_boundary_condition
        }

    @staticmethod
    def inside(heat_information):
        inside_temperature = heat_information['main']['inside_temperature']
        inside_heater_power = heat_information['main']['inside_heater_power']

        if inside_temperature is not None:
            bc = BoundaryConditionName.dirichlet.value
        elif inside_heater_power is not None:
            bc = BoundaryConditionName.neumann.value
        else:
            bc = None
        return bc

    @staticmethod
    def outside(heat_information):
        outside_temperature = heat_information['main']['outside_temperature']
        outside_heater_power = heat_information['main']['outside_heater_power']

        if outside_temperature is not None:
            bc = BoundaryConditionName.dirichlet.value
        elif outside_heater_power is not None:
            bc = BoundaryConditionName.neumann.value
        else:
            bc = None
        return bc
