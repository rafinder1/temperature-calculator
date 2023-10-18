import logging
from enum import Enum

from pandas import DataFrame

from calculator.shared_data.method_calc.fem import FEM
from calculator.shared_data.outside_inside_thermal_data import OutsideInsideThermalData


class MethodCalculator(Enum):
    FINITE_ELEMENT_METHOD = 'finite_element_method'
    THERMAL_RESISTANCE_METHOD = 'thermal_resistance_method'

    @classmethod
    def get_all_method(cls):
        return list(cls)

    @classmethod
    def get_value_method(cls):
        methods = cls.get_all_method()
        return [method.value for method in methods]

    @classmethod
    def calculate_by_method(cls, method: str, data_building_partition: DataFrame,
                            outside_inside_thermal_data: OutsideInsideThermalData,
                            boundary_condition: str) -> DataFrame:
        if method == cls.FINITE_ELEMENT_METHOD.value:
            return FEM.calculate(data_building_partition, outside_inside_thermal_data,
                                 boundary_condition)
        elif method == cls.THERMAL_RESISTANCE_METHOD.value:
            return cls.thermal_resistance_method()
        else:
            raise ValueError("This method does not exist")

    @staticmethod
    def thermal_resistance_method() -> DataFrame:
        logging.info("Thermal resistance calculations")
        return DataFrame
