import pandas as pd

column_names = ["type_layer", "name_layer", "thickness", "thermal_conductivity", "cost"]
type_layers = ["tynk", "mur", "ocieplenie", 'tynk']
name_layers = ["Tynk gipsowy", "Beton Komórkowy", "Płyta styropianowa EPS 80-042 FASADA λ 0.042",
               "Tynk silikatowy CERESIT CT74 1.5mm"]
thickness = [0.02, 0.24, 0.15, 0.015]
thermal_conductivity = [0.4, 0.16, 0.042, 0.8]
cost = [32.81, 121.43, 33.95, 30]

data_building_partition = pd.DataFrame(
    data=list(zip(type_layers, name_layers, thickness, thermal_conductivity, cost)),
    columns=column_names)
