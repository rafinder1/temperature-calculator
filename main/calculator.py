from pandas import DataFrame
from main.config import MethodName
from main.method_calculator import MethodCalculator
from main.boundary_condition_definer import BoundaryConditionDefiner


class TempCalculator:

    @staticmethod
    def calculate(data_building_partition: DataFrame, heat_information: dict, method: MethodName) -> DataFrame:

        boundary_condition = BoundaryConditionDefiner.define(heat_information)

        selected_method = MethodCalculator.select_calculation_method(method)

        result = selected_method(data_building_partition, heat_information, boundary_condition)

        return DataFrame
