from pandas import DataFrame
from calculator.basic.config import MethodName


class MultiVariantsCalculator:
    @staticmethod
    def change_polystyrene(data_building_partition: DataFrame, heat_information: dict, polystyrene_data: DataFrame,
                           method: MethodName) -> DataFrame:
        print(polystyrene_data)
        return DataFrame
