from enum import Enum


class MethodName(Enum):
    finite_element_method = "finite_element_method"


class BoundaryConditionName(Enum):
    neumann = "neumann"
    dirichlet = "dirichlet"
    inside = "inside_boundary_condition"
    outside = "outside_boundary_condition"


class ConditionsInBuilding(Enum):
    inside_temperature = "inside_temperature"
    outside_temperature = "outside_temperature"
    inside_heater_power = "inside_heater_power"
    outside_heater_power = "outside_heater_power"


air_and_heater_param = [
    {'type_layer': 'air', 'name_layer': 'air', 'thickness': 0.1, 'thermal_conductivity': 0.025},
    {'type_layer': 'heater', 'name_layer': 'heater', 'thickness': 0.1, 'thermal_conductivity': 50}
]
