import logging
import sys

from pandas import DataFrame

from calculator.basic.calculator import TempCalculator
from calculator.config import GLOBAL_LOGGING_LEVEL
from calculator.multivariants.config import Rsi, Rse

logging.basicConfig(stream=sys.stdout, level=GLOBAL_LOGGING_LEVEL)


class MultiVariantsCalculator:
    @staticmethod
    def change_polystyrene(data_building_partition: DataFrame, heat_information: dict, polystyrene_data: DataFrame,
                           method: str) -> DataFrame:
        try:
            logging.info(f'Multi-variant analysis for a given building partition: {data_building_partition}.'
                         f'For the conditions around it: {heat_information}')
            if len(data_building_partition) == 1:
                if data_building_partition['type_layer'].isin(['ocieplenie']).any():
                    raise ValueError("Define only polystyrene - multivariate analysis cannot be performed")
                else:
                    index_polystyrene = len(data_building_partition) + 1
            else:
                index_polystyrene = data_building_partition[data_building_partition['type_layer'] == 'ocieplenie'].index

            if heat_information['outside_temperature'] is None or heat_information['outside_temperature'] == "":
                default_outside_temperature = -20
                logging.warning(
                    f'Outside Temperature is not defined. Take the default value equal {default_outside_temperature}°C')

                heat_information['outside_temperature'] = default_outside_temperature
            if heat_information['inside_heater_power'] is None or heat_information['inside_heater_power'] == "":
                default_inside_heater_power = 80
                logging.warning(
                    f'Inside Heater Power is not defined. Take the default value equal {default_inside_heater_power} W/m2')

                heat_information['inside_heater_power'] = default_inside_heater_power

            for number_row, polystyrene_param in polystyrene_data.iterrows():
                data_building_partition.loc[index_polystyrene, 'name_layer'] = polystyrene_param['name_layer']
                data_building_partition.loc[index_polystyrene, 'thickness'] = polystyrene_param['thickness']
                data_building_partition.loc[index_polystyrene, 'thermal_conductivity'] = polystyrene_param[
                    'thermal_conductivity']

                heat_transfer_coefficient = MultiVariantsCalculator.calc_heat_transfer_coefficient(
                    data_building_partition)
                temperatures_all_layers = TempCalculator.calculate(data_building_partition, heat_information, method)

                temperature_last_layer = temperatures_all_layers.iloc[-1]['temperatures']

                polystyrene_data.loc[number_row, 'temperatures'] = temperature_last_layer

                if heat_transfer_coefficient > 0.2:
                    polystyrene_data.loc[number_row, 'comments'] = 'U>0.2'
                if temperature_last_layer > 30:
                    polystyrene_data.loc[number_row, 'comments'] = 'temperature above 30'
        except ValueError as e:
            return data_building_partition
        return polystyrene_data

    @staticmethod
    def calc_heat_transfer_coefficient(data_building_partition):
        return 1 / (Rsi + Rse + sum(
            (data_building_partition['thickness']) / data_building_partition['thermal_conductivity']))
