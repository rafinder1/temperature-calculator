from tests.multivariants.polystyrene_data import polystyrene_data
import copy
temperatures = [17.31, 19.22]
comments = ['U>0.2', None]

expected = copy.deepcopy(polystyrene_data)
expected['temperatures'] = temperatures
expected['comments'] = comments
