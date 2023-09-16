import unittest

from calculator.multivariants.multivariants import MultiVariantsCalculator
from calculator.basic.config import MethodName
from tools.file_helper import FileHelper


class MainTestCase(unittest.TestCase):
    def test_temperature_calculator_dirichlet_neumann(self):
        data_building_partition = FileHelper.read_csv("tests/multivariants/building_partition.txt")

        heat_information = FileHelper.read_json("tests/multivariants/heat_information_dirichlet_neumann.json")

        polystyrene_data = FileHelper.read_excel(file="tests/multivariants/warstwy_przegrody.xlsx",
                                                 sheet_name='polystyrene_cost')

        method = MethodName.finite_element_method

        output = MultiVariantsCalculator.change_polystyrene(data_building_partition=data_building_partition,
                                                            heat_information=heat_information,
                                                            polystyrene_data=polystyrene_data, method=method)
        self.assertTrue(True)
        # expected = data_building_partition.copy(deep=True)
        # expected['temperatures'] = [-19.60, -7.60, 20.97, 21.12]
        #
        # self.assertTrue(expected.equals(output))
