import logging

from pandas import DataFrame, Series

from calculator.basic.calculator import TempCalculator
from calculator.config import GLOBAL_LOGGING_LEVEL
from calculator.multivariants.config import Rsi, Rse
from calculator.shared_data.method_calculator import MethodCalculator
from calculator.shared_data.outside_inside_thermal_data import OutsideInsideThermalData

logging.basicConfig(level=GLOBAL_LOGGING_LEVEL)


class MultiVariantsCalculator:
    @classmethod
    def change_polystyrene(cls, data_building_partition: DataFrame,
                           outside_inside_thermal_data: OutsideInsideThermalData,
                           polystyrene_data: DataFrame,
                           method: str) -> DataFrame:
        try:
            logging.info('START CALCULATION: Multi-variant analysis')
            logging.info(
                f'Multi-variant analysis for a given building partition: {data_building_partition}.'
                f'For the conditions around it: {outside_inside_thermal_data}')

            cls.validate_data(data_building_partition=data_building_partition,
                              outside_inside_thermal_data=outside_inside_thermal_data,
                              polystyrene_data=polystyrene_data, method=method)

            for number_row, polystyrene_param in polystyrene_data.iterrows():
                update_data_bp = cls.update_polystyrene_data(data=data_building_partition,
                                                             parameters=polystyrene_param)

                temperature_last_layer = cls.get_temperature_from_last_layer(
                    method=method, outside_inside_thermal_data=outside_inside_thermal_data,
                    data_bp=update_data_bp)

                polystyrene_data.loc[number_row, 'temperatures'] = temperature_last_layer

                polystyrene_data.loc[
                    number_row, 'comments'] = cls.validate_heat_transfer_coefficient(
                    data_bp=update_data_bp)
            logging.info('FINISH CALCULATION: Multi-variant analysis')
        except ValueError as error:
            pass
        return polystyrene_data

    @classmethod
    def get_temperature_from_last_layer(cls, method: str,
                                        outside_inside_thermal_data: OutsideInsideThermalData,
                                        data_bp: DataFrame) -> float:
        temperatures_all_layers = TempCalculator.calculate(
            data_building_partition=data_bp,
            outside_inside_thermal_data=outside_inside_thermal_data, method=method)

        temperature_last_layer = temperatures_all_layers.iloc[-1]['temperatures']
        return temperature_last_layer

    @classmethod
    def validate_heat_transfer_coefficient(cls, data_bp: DataFrame) -> str:
        heat_transfer_coefficient = cls.calc_heat_transfer_coefficient(
            data_bp)

        return cls.check_heat_transfer_coefficient(heat_transfer_coefficient)

    @classmethod
    def check_heat_transfer_coefficient(cls, heat_transfer_coefficient: float) -> str:
        if heat_transfer_coefficient > 0.2:
            return 'U>0.2'

    @classmethod
    def update_polystyrene_data(cls, data: DataFrame, parameters: Series) -> DataFrame:
        index = cls.find_polystyrene_in_data(data_building_partition=data)

        data.loc[index, 'name_layer'] = parameters['name_layer']
        data.loc[index, 'thickness'] = parameters['thickness']
        data.loc[index, 'thermal_conductivity'] = parameters['thermal_conductivity']

        return data

    @classmethod
    def validate_data(cls, data_building_partition: DataFrame,
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

    @classmethod
    def validate_name_method(cls, method: str):
        value_method = MethodCalculator.get_value_method()
        if method not in value_method:
            raise NameError(f'Wrong name method: {method}. You can choose: {value_method}')

    @classmethod
    def validate_type_data(cls, data, data_type):
        if type(data) is not data_type:
            raise TypeError(f"Data has wrong type. {data_type} != {type(data)}")

    @classmethod
    def validate_outside_inside_thermal_data(cls,
                                             outside_inside_thermal_data:
                                             OutsideInsideThermalData) -> None:
        outside_inside_thermal_data.validated_data_presence()

    @staticmethod
    def find_polystyrene_in_data(data_building_partition: DataFrame) -> int:

        if len(data_building_partition) == 1:
            index_polystyrene = len(data_building_partition) + 1
        else:
            index_polystyrene = data_building_partition[
                data_building_partition['type_layer'] == 'ocieplenie'].index
        return index_polystyrene

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

    @staticmethod
    def calc_heat_transfer_coefficient(data_bp):
        return 1 / (Rsi + Rse + sum((data_bp['thickness']) / data_bp['thermal_conductivity']))
