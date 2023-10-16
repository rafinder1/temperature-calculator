import pandas as pd

column_names = ["name_layer", "thickness", "thermal_conductivity"]

name_layer = ["styropian", "styropian"]

thickness = [0.13, 0.14]
thermal_conductivity = [0.042, 0.042]

polystyrene_data = pd.DataFrame(
    data=list(zip(name_layer, thickness, thermal_conductivity)),
    columns=column_names)
