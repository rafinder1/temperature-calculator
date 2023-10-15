from pandas.testing import assert_frame_equal

from calculator.multivariants.multivariants import MultiVariantsCalculator
from tests.multivariants.building_partition import data_building_partition
from tests.multivariants.expected_temperatures import expected
from tests.multivariants.outside_inside_thermal_data import outside_inside_thermal_data
from tests.multivariants.polystyrene_data import polystyrene_data


def test_multi_variants_calculator():
    # given
    method = 'finite_element_method'

    # when
    output = MultiVariantsCalculator.change_polystyrene(
        data_building_partition=data_building_partition,
        outside_inside_thermal_data=outside_inside_thermal_data,
        polystyrene_data=polystyrene_data, method=method)
    # then
    assert_frame_equal(expected, output)
