import unittest

import pandas as pd

from calculator.calculator import TempCalculator
from calculator.config import MethodName
from tools.file_helper import FileHelper


class MainTestCase(unittest.TestCase):
    def test_temperature_calculator_dirichlet_neumann(self):
        data_building_partition = FileHelper.read_csv("tests/building_partition.txt")

        heat_information = FileHelper.read_json("tests/heat_information_dirichlet_neumann.json")

        method = MethodName.finite_element_method

        output = TempCalculator.calculate(data_building_partition, heat_information, method)

        expected = data_building_partition.copy(deep=True)
        expected['temperatures'] = [-19.60, -7.60, 20.97, 21.12]

        self.assertTrue(expected.equals(output))

    def test_temperature_calculator_dirichlet_dirichlet(self):
        data_building_partition = FileHelper.read_csv("tests/building_partition.txt")

        heat_information = FileHelper.read_json("tests/heat_information_dirichlet_dirichlet.json")

        method = MethodName.finite_element_method

        output = TempCalculator.calculate(data_building_partition, heat_information, method)

        expected = data_building_partition.copy(deep=True)
        expected['temperatures'] = [-19.61, -7.94, 19.85, 20.00]

        self.assertTrue(expected.equals(output))
