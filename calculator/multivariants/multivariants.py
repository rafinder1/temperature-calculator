import logging
import sys

from pandas import DataFrame

from calculator.basic.calculator import TempCalculator
from calculator.config import GLOBAL_LOGGING_LEVEL
from calculator.multivariants.config import Rsi, Rse
from calculator.shared_data.outside_inside_thermal_data import OutsideInsideThermalData

logging.basicConfig(level=GLOBAL_LOGGING_LEVEL)


class MultiVariantsCalculator:
    @classmethod
    def change_polystyrene(cls, data_building_partition: DataFrame,
                           outside_inside_thermal_data: OutsideInsideThermalData,
                           polystyrene_data: DataFrame,
                           method: str) -> DataFrame:
        try:
            logging.info(
                f'Multi-variant analysis for a given building partition: {data_building_partition}.'
                f'For the conditions around it: {outside_inside_thermal_data}')

            cls.validate_data(data_building_partition, outside_inside_thermal_data,
                              polystyrene_data)

            index_polystyrene = cls.find_polystyrene_in_data(
                data_building_partition=data_building_partition)

            for number_row, polystyrene_param in polystyrene_data.iterrows():
                data_building_partition.loc[index_polystyrene, 'name_layer'] = polystyrene_param[
                    'name_layer']
                data_building_partition.loc[index_polystyrene, 'thickness'] = polystyrene_param[
                    'thickness']
                data_building_partition.loc[index_polystyrene, 'thermal_conductivity'] = \
                    polystyrene_param[
                        'thermal_conductivity']

                heat_transfer_coefficient = MultiVariantsCalculator.calc_heat_transfer_coefficient(
                    data_building_partition)
                temperatures_all_layers = TempCalculator.calculate(data_building_partition,
                                                                   outside_inside_thermal_data,
                                                                   method)
                logging.info(temperatures_all_layers)

                temperature_last_layer = temperatures_all_layers.iloc[-1]['temperatures']

                polystyrene_data.loc[number_row, 'temperatures'] = temperature_last_layer

                if heat_transfer_coefficient > 0.2:
                    polystyrene_data.loc[number_row, 'comments'] = 'U>0.2'
                if temperature_last_layer > 30:
                    polystyrene_data.loc[number_row, 'comments'] = 'temperature above 30'
        except ValueError as error:
            logging.error(error)
            return data_building_partition
        return polystyrene_data

    @classmethod
    def validate_data(cls, data_building_partition: DataFrame,
                      outside_inside_thermal_data: OutsideInsideThermalData,
                      polystyrene_data: DataFrame):

        cls.validate_non_empty_data(data=polystyrene_data)

        cls.validate_non_empty_data(data=data_building_partition)
        cls.validate_contains_only_polystyrene(data_building_partition=data_building_partition)

        cls.validate_outside_inside_thermal_data(
            outside_inside_thermal_data=outside_inside_thermal_data)

        logging.info("Provided data is OK")

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
    def validate_contains_only_polystyrene(data_building_partition: DataFrame) -> bool:
        if len(data_building_partition) == 1:
            if data_building_partition['type_layer'].isin(['ocieplenie']).any():
                raise ValueError(
                    "Define only polystyrene - multivariate analysis cannot be performed")

    @staticmethod
    def calc_heat_transfer_coefficient(data_building_partition):
        return 1 / (Rsi + Rse + sum(
            (data_building_partition['thickness']) / data_building_partition[
                'thermal_conductivity']))
