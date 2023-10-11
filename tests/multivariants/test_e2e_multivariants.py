import unittest
from pandas.testing import assert_frame_equal
from calculator.multivariants.multivariants import MultiVariantsCalculator
from calculator.basic.config import MethodName
from tools.file_helper import FileHelper


class MainTestCase(unittest.TestCase):
    def test_multi_variants_calculator(self):
        expected = FileHelper.read_csv("tests/multivariants/expected_temperatures.csv")

        data_building_partition = FileHelper.read_csv("tests/multivariants/building_partition.txt")

        heat_information = FileHelper.read_json("tests/multivariants/heat_information_dirichlet_neumann.json")

        polystyrene_data = FileHelper.read_excel(file="tests/multivariants/warstwy_przegrody.xlsx",
                                                 sheet_name='polystyrene_cost')

        method = 'finite_element_method'

        output = MultiVariantsCalculator.change_polystyrene(data_building_partition=data_building_partition,
                                                            heat_information=heat_information,
                                                            polystyrene_data=polystyrene_data, method=method)

        assert_frame_equal(expected, output)
