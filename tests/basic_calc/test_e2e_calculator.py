import unittest

from calculator.basic.calculator import TempCalculator
from tools.file_helper import FileHelper


class MainTestCase(unittest.TestCase):
    def test_temperature_calculator_dirichlet_neumann(self):
        data_building_partition = FileHelper.read_csv("tests/basic_calc/building_partition.txt")

        heat_information = FileHelper.read_json("tests/basic_calc/heat_information_dirichlet_neumann.json")

        method = 'finite_element_method'

        output = TempCalculator.calculate(data_building_partition, heat_information, method)

        expected = data_building_partition.copy(deep=True)
        expected['temperatures'] = [-19.60, -7.60, 20.97, 21.12]

        self.assertTrue(expected.equals(output))

    def test_temperature_calculator_dirichlet_dirichlet(self):
        data_building_partition = FileHelper.read_csv("tests/basic_calc/building_partition.txt")

        heat_information = FileHelper.read_json("tests/basic_calc/heat_information_dirichlet_dirichlet.json")

        method = 'finite_element_method'

        output = TempCalculator.calculate(data_building_partition, heat_information, method)

        expected = data_building_partition.copy(deep=True)
        expected['temperatures'] = [-19.61, -7.94, 19.85, 20.00]

        self.assertTrue(expected.equals(output))
