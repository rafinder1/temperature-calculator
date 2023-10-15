import unittest

from calculator.basic.calculator import TempCalculator
from calculator.shared_data.outside_inside_thermal_data import OutsideInsideThermalData
from tools.file_helper import FileHelper


class MainTestCase(unittest.TestCase):
    def test_temperature_calculator_dirichlet_neumann(self):
        data_building_partition = FileHelper.read_csv("tests/basic_calc/building_partition.txt")

        outside_inside_thermal_data = OutsideInsideThermalData(
            OUTSIDE_TEMPERATURE=-20,
            INSIDE_HEATER_POWER=80)

        method = 'finite_element_method'

        output = TempCalculator.calculate(data_building_partition, outside_inside_thermal_data,
                                          method)

        expected = data_building_partition.copy(deep=True)
        expected['temperatures'] = [-19.60, -7.60, 20.97, 21.12]

        self.assertTrue(expected.equals(output))

    def test_temperature_calculator_dirichlet_dirichlet(self):
        data_building_partition = FileHelper.read_csv("tests/basic_calc/building_partition.txt")

        outside_inside_thermal_data = OutsideInsideThermalData(
            OUTSIDE_TEMPERATURE=-20,
            INSIDE_TEMPERATURE=20
        )

        method = 'finite_element_method'

        output = TempCalculator.calculate(data_building_partition, outside_inside_thermal_data, method)

        expected = data_building_partition.copy(deep=True)
        expected['temperatures'] = [-19.61, -7.94, 19.85, 20.00]

        self.assertTrue(expected.equals(output))
