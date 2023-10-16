import logging

from pandas import DataFrame

from calculator.config import GLOBAL_LOGGING_LEVEL
from calculator.shared_data.method_calculator import MethodCalculator
from calculator.shared_data.outside_inside_thermal_data import OutsideInsideThermalData

logging.basicConfig(level=GLOBAL_LOGGING_LEVEL)


class DataValidator:
    @classmethod
    def validate_mvc_data(cls, data_building_partition: DataFrame,
                          outside_inside_thermal_data: OutsideInsideThermalData,
                          polystyrene_data: DataFrame,
                          method: str):

        cls.validate_type_data(data=data_building_partition, data_type=DataFrame)
        cls.validate_type_data(data=outside_inside_thermal_data, data_type=OutsideInsideThermalData)
        cls.validate_type_data(data=polystyrene_data, data_type=DataFrame)
        cls.validate_type_data(data=method, data_type=str)

        cls.validate_name_method(method=method)
        cls.validate_non_empty_data(data=polystyrene_data)

        cls.validate_non_empty_data(data=data_building_partition)
        cls.validate_contains_only_polystyrene(data_bp=data_building_partition)

        cls.validate_outside_inside_thermal_data(
            outside_inside_thermal_data=outside_inside_thermal_data)

        logging.info("Provided data is OK")

    @staticmethod
    def validate_name_method(method: str):
        value_method = MethodCalculator.get_value_method()
        if method not in value_method:
            raise NameError(f'Wrong name method: {method}. You can choose: {value_method}')

    @staticmethod
    def validate_type_data(data, data_type):
        if type(data) is not data_type:
            raise TypeError(f"Data has wrong type. {data_type} != {type(data)}")

    @staticmethod
    def validate_non_empty_data(data: DataFrame):
        if len(data) == 0:
            logging.error("Data has not been defined")
            raise ValueError("Data has not been defined")

    @staticmethod
    def validate_contains_only_polystyrene(data_bp: DataFrame) -> bool:
        if len(data_bp) == 1:
            if data_bp['type_layer'].isin(['ocieplenie']).any():
                raise ValueError(
                    "Define only polystyrene - multivariate analysis cannot be performed")

    @classmethod
    def validate_outside_inside_thermal_data(cls,
                                             outside_inside_thermal_data:
                                             OutsideInsideThermalData) -> None:
        outside_inside_thermal_data.validated_data_presence()
