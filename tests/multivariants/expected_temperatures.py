import copy

from tests.multivariants.polystyrene_data import polystyrene_data

temperatures = [17.31, 19.22]
U_is_above_0_2 = [True, False]

expected = copy.deepcopy(polystyrene_data)
expected['temperatures'] = temperatures
expected["U_is_above_0_2"] = U_is_above_0_2
