from pandas import DataFrame

from calculator.basic.method_calculator import MethodCalculator
from calculator.shared_data.boundary_condition_definer import BoundaryConditionDefiner
from calculator.shared_data.outside_inside_thermal_data import OutsideInsideThermalData


class TempCalculator:

    @classmethod
    def calculate(cls, data_building_partition: DataFrame,
                  outside_inside_thermal_data: OutsideInsideThermalData, method: str) -> DataFrame:
        """
        The method computes the temperature distribution across each layer provided through inputs.
        Under the data_building_partition parameter, there's a DataFrame containing layer types,
        layer names,
        thickness, thermal conductivity, and cost per square meter. The heat_information
        parameter holds data about
        heat, including conductivity, temperature, and/or heat transfer. The boundary_condition
        parameter contains
        information about boundary conditions, describing the conditions within the environment.


        :param data_building_partition: DataFrame containing layer types, layer names, thickness,
        thermal conductivity,
        and cost per square meter.
        :param outside_inside_thermal_data: A dictionary containing information about temperature
        and/or
        heat transfer.
        :param method: An input provided as a string that specifies the name of the method.
        :return: The function returns all of this data expanded to include temperature distribution.
        """
        outside_inside_thermal_data.validated_data_presence()
        boundary_condition = BoundaryConditionDefiner.define(
            outside_inside_thermal_data=outside_inside_thermal_data)

        result = MethodCalculator.calculate_by_method(method=method,
                                                      data_building_partition=data_building_partition,
                                                      outside_inside_thermal_data=outside_inside_thermal_data,
                                                      boundary_condition=boundary_condition)

        return result
