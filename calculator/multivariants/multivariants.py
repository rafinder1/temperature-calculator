import logging

from pandas import DataFrame, Series

from calculator.basic.calculator import TempCalculator
from calculator.config import GLOBAL_LOGGING_LEVEL
from calculator.multivariants.config import Rsi, Rse
from calculator.shared_data.data_validator import DataValidator
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

            DataValidator.validate_mvc_data(data_building_partition=data_building_partition,
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
        except ValueError:
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

    @staticmethod
    def find_polystyrene_in_data(data_building_partition: DataFrame) -> int:

        if len(data_building_partition) == 1:
            index_polystyrene = len(data_building_partition) + 1
        else:
            index_polystyrene = data_building_partition[
                data_building_partition['type_layer'] == 'ocieplenie'].index
        return index_polystyrene

    @staticmethod
    def calc_heat_transfer_coefficient(data_bp):
        return 1 / (Rsi + Rse + sum((data_bp['thickness']) / data_bp['thermal_conductivity']))
