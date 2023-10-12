from enum import Enum


class ConditionsInBuilding(Enum):
    INSIDE_TEMPERATURE = "inside_temperature"
    OUTSIDE_TEMPERATURE = "outside_temperature"
    INSIDE_HEATER_POWER = "inside_heater_power"
    outside_heater_power = "outside_heater_power"


air_and_heater_param = [
    {'type_layer': 'air', 'name_layer': 'air', 'thickness': 0.1, 'thermal_conductivity': 0.025},
    {'type_layer': 'heater', 'name_layer': 'heater', 'thickness': 0.1, 'thermal_conductivity': 50}
]

area = 1
