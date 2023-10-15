import pandas as pd
column_names = ["name_layer", "thickness", "thermal_conductivity", "cost"]

name_layer = ["styropian"] * 21

thickness = [0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15,
             0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18]
thermal_conductivity = [0.042] * 8 + [0.031] * 6 + [0.038] * 7
cost = [29.42, 31.69, 33.95, 36.21, 38.47, 40.47, 43, 45.27, 31.98, 35.18, 38.38, 41.58, 44.77,
        47.97, 33.95, 36.78, 39.61, 42.44, 45.27, 48.09, 50.92]

polystyrene_data = pd.DataFrame(
    data=list(zip(name_layer, thickness, thermal_conductivity, cost)),
    columns=column_names)
