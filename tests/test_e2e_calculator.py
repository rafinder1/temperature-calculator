import unittest

import pandas as pd

from main.calculator import TempCalculator
from tools.file_helper import FileHelper


class MainTestCase(unittest.TestCase):
    def test_temperature_calculator(self):
        expected = pd.DataFrame
        data_building_partition = FileHelper.read_csv("tests/building_partition.txt")
        heat_information = dict()
        print(data_building_partition)
        data_frame = TempCalculator.calculate(data_building_partition, heat_information)
        self.assertEqual(expected, data_frame)
