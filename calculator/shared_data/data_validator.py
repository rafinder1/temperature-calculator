import logging

from pandas import DataFrame

from calculator.config import GLOBAL_LOGGING_LEVEL
from calculator.shared_data.method_calculator import MethodCalculator
from calculator.shared_data.outside_inside_thermal_data import OutsideInsideThermalData

logging.basicConfig(level=GLOBAL_LOGGING_LEVEL)


class DataValidator:
    @classmethod
    def validate_data_from_calculator(cls, data_building_partition: DataFrame,
                                      outside_inside_thermal_data: OutsideInsideThermalData,
                                      method: str,
                                      polystyrene_data: DataFrame = None
                                      ):

        cls.validate_type_data(data=method, data_type=str)
        cls.validate_name_method(method=method)

        cls.validate_type_data(data=data_building_partition, data_type=DataFrame)
        cls.validate_non_empty_data(data=data_building_partition)
        cls.validate_contains_only_polystyrene(data_bp=data_building_partition)

        cls.validate_outside_inside_thermal_data(
            outside_inside_thermal_data=outside_inside_thermal_data)
        cls.validate_type_data(data=outside_inside_thermal_data, data_type=OutsideInsideThermalData)

        if polystyrene_data is not None:
            cls.validate_non_empty_data(data=polystyrene_data)
            cls.validate_type_data(data=polystyrene_data, data_type=DataFrame)

        logging.info("Provided data is OK")

    @classmethod
    def validate_data_in_ap(cls, wall_surface: float, price_square_meter: float,
                            amount_polystyrene_in_one_package: float):

        cls.validate_type_data(data=wall_surface, data_type=float)
        cls.validate_type_data(data=price_square_meter, data_type=float)
        cls.validate_type_data(data=amount_polystyrene_in_one_package, data_type=float)

        cls.validate_value_is_positive(value=wall_surface)
        cls.validate_value_is_positive(value=price_square_meter)
        cls.validate_value_is_positive(value=amount_polystyrene_in_one_package)

        logging.info("Provided data is OK")

    @staticmethod
    def validate_name_method(method: str):
        value_method = MethodCalculator.get_value_method()
        if method not in value_method:
            raise NameError(f'Wrong name method: {method}. You can choose: {value_method}')

    @staticmethod
    def validate_value_is_positive(value: float):
        if value <= 0:
            raise ValueError("Value must be greater than 0")

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
