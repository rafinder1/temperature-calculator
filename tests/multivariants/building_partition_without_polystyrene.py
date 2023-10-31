import pandas as pd

column_names = ["type_layer", "name_layer", "thickness", "thermal_conductivity", "cost"]
type_layers = ["tynk", "mur", 'tynk']
name_layers = ["Cementowo - wapienny", "Porotherm Dryfix", "Cementowo - wapienny"]
thickness = [0.02, 0.425, 0.02]
thermal_conductivity = [0.45, 0.076, 0.45]
cost = [2.83, 553.28, 2.83]

data_building_partition_without_polystyrene = pd.DataFrame(
    data=list(zip(type_layers, name_layers, thickness, thermal_conductivity, cost)),
    columns=column_names)
