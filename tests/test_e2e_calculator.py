import unittest

import pandas as pd

from main.calculator import TempCalculator


class MainTestCase(unittest.TestCase):
    def test_temperature_calculator(self):
        expected = pd.DataFrame
        data_building_partition = pd.DataFrame
        heat_information = dict()

        data_frame = TempCalculator.calculate(data_building_partition, heat_information)
        self.assertEqual(expected, data_frame)
