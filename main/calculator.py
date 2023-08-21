from pandas import DataFrame
from main.config import MethodSelector
from main.method import MethodCalculator


class TempCalculator:
    @staticmethod
    def calculate(data_building_partition: DataFrame, heat_information: dict, method: MethodSelector) -> DataFrame:
        selected_method = getattr(MethodCalculator, method.value)
        result = selected_method()
        print(result)
        return DataFrame
