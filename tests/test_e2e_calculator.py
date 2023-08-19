import unittest

import pandas as pd

from main.calculator import TempCalculator


class MainTestCase(unittest.TestCase):
    def test_temperature_calculator(self):
        expected = "This is Temperature calculator - package"
        data_building_partition = pd.DataFrame
        heat_information = dict()

        txt = TempCalculator.calculate(data_building_partition, heat_information)
        self.assertEqual(expected, txt)
