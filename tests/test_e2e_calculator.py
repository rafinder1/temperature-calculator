import unittest

import pandas as pd

from main.calculator import TempCalculator
from main.config import MethodSelector
from tools.file_helper import FileHelper


class MainTestCase(unittest.TestCase):
    def test_temperature_calculator(self):
        expected = pd.DataFrame
        data_building_partition = FileHelper.read_csv("tests/building_partition.txt")

        heat_information = FileHelper.read_json("tests/heat_information.json")

        method = MethodSelector.finite_element_method

        data_frame = TempCalculator.calculate(data_building_partition, heat_information, method)

        self.assertEqual(expected, data_frame)
