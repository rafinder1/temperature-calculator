import pandas as pd

air_and_heater_param = [
    {'type_layer': 'air', 'name_layer': 'air', 'thickness': 0.1, 'thermal_conductivity': 0.025},
    {'type_layer': 'heater', 'name_layer': 'heater', 'thickness': 0.1, 'thermal_conductivity': 50}
]

air_heater_dataframe = pd.DataFrame(air_and_heater_param)

area = 1
