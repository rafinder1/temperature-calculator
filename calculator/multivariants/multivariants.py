from pandas import DataFrame
import numpy as np
from calculator.basic.config import MethodName
from calculator.basic.calculator import TempCalculator
from calculator.multivariants.config import Rsi, Rse


class MultiVariantsCalculator:
    @staticmethod
    def change_polystyrene(data_building_partition: DataFrame, heat_information: dict, polystyrene_data: DataFrame,
                           method: MethodName) -> DataFrame:
        try:
            if len(data_building_partition) == 1:
                if data_building_partition['type_layer'].isin(['ocieplenie']).any():
                    raise ValueError("Define only polystyrene - multivariate analysis cannot be performed")
                else:
                    index_polystyrene = len(data_building_partition) + 1
            else:
                index_polystyrene = data_building_partition[data_building_partition['type_layer'] == 'ocieplenie'].index

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
            print(e)
            return data_building_partition
        return polystyrene_data

    @staticmethod
    def calc_heat_transfer_coefficient(data_building_partition):
        return 1 / (Rsi + Rse + sum(
            (data_building_partition['thickness']) / data_building_partition['thermal_conductivity']))
