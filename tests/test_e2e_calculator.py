import unittest

import pandas as pd

from main.calculator import TempCalculator
from main.config import MethodName
from tools.file_helper import FileHelper


class MainTestCase(unittest.TestCase):
    def test_temperature_calculator(self):
        data_building_partition = FileHelper.read_csv("tests/building_partition.txt")

        heat_information = FileHelper.read_json("tests/heat_information.json")

        method = MethodName.finite_element_method

        data_frame = TempCalculator.calculate(data_building_partition, heat_information, method)

        expected = data_building_partition.copy(deep=True)
        expected['temperatures'] = [-19.60, -7.60, 20.97, 21.12]

        self.assertTrue(expected.equals(data_frame))
