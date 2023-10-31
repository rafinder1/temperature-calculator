import copy

from tests.multivariants.polystyrene_data import polystyrene_data

temperatures = [25.45, 25.45]
U_is_above_0_2 = [False, False]

expected_wo_polystyrene = copy.deepcopy(polystyrene_data)
expected_wo_polystyrene['temperatures'] = temperatures
expected_wo_polystyrene["U_is_above_0_2"] = U_is_above_0_2
