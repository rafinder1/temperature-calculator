from tests.multivariants.polystyrene_data import polystyrene_data
import copy
temperatures = [17.31, 19.22, 21.12, 23.03, 24.93, 26.84, 28.74, 30.65, 18.36, 20.94, 23.52, 26.10,
                28.68, 31.26, 17.81, 19.92, 22.02,24.13,26.23,28.34,30.44]
comments = ['U>0.2', None, None, None, None, None, None, 'temperature above 30', 'U>0.2', None,
            None, None, None, 'temperature above 30', 'U>0.2', None, None, None, None, None,
            'temperature above 30']

expected = copy.deepcopy(polystyrene_data)
expected['temperatures'] = temperatures
expected['comments'] = comments
