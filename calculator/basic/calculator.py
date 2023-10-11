from pandas import DataFrame
from calculator.basic.config import MethodName
from calculator.basic.method_calculator import MethodCalculator
from calculator.basic.boundary_condition_definer import BoundaryConditionDefiner


class TempCalculator:

    @staticmethod
    def calculate(data_building_partition: DataFrame, heat_information: dict, method: str) -> DataFrame:
        """
        The method computes the temperature distribution across each layer provided through inputs.
        Under the data_building_partition parameter, there's a DataFrame containing layer types, layer names,
        thickness, thermal conductivity, and cost per square meter. The heat_information parameter holds data about
        heat, including conductivity, temperature, and/or heat transfer. The boundary_condition parameter contains
        information about boundary conditions, describing the conditions within the environment.


        :param data_building_partition: DataFrame containing layer types, layer names, thickness, thermal conductivity,
        and cost per square meter.
        :param heat_information: A dictionary containing information about temperature and/or heat transfer.
        :param method: An input provided as a string that specifies the name of the method.
        :return: The function returns all of this data expanded to include temperature distribution.
        """

        boundary_condition = BoundaryConditionDefiner.define(heat_information=heat_information)

        result = MethodCalculator.calculate_by_method(method, data_building_partition, heat_information, boundary_condition)

        return result
