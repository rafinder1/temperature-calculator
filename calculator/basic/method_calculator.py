import logging
from enum import Enum

import numpy as np
import pandas as pd
from pandas import DataFrame

from calculator.basic.boundary_condition_definer import BoundaryConditionDefiner
from calculator.basic.config import ConditionsInBuilding, air_and_heater_param, area


class MethodCalculator(Enum):
    FINITE_ELEMENT_METHOD = 'finite_element_method'
    THERMAL_RESISTANCE_METHOD = 'thermal_resistance_method'

    @classmethod
    def calculate_by_method(cls, method: str, data_building_partition: DataFrame, heat_information: dict,
                            boundary_condition: str) -> DataFrame:
        if method == cls.FINITE_ELEMENT_METHOD.value:
            return cls.finite_element_method(data_building_partition, heat_information, boundary_condition)
        elif method == cls.THERMAL_RESISTANCE_METHOD.value:
            return cls.thermal_resistance_method()
        else:
            raise ValueError("This method does not exist")

    @staticmethod
    def finite_element_method(data_building_partition: DataFrame, heat_information: dict, boundary_condition: dict):
        """
        The finite element method in the 1D dimension was used to calculate the heat
        """
        logging.info("Finite element calculations")

        data_building_partition_with_air_heater = (MethodCalculator
                                                   .add_air_and_metal_heater(boundary_condition=boundary_condition,
                                                                             data_building_partition=data_building_partition))
        data_building_partition_with_temperatures = (
            MethodCalculator.create_equation_and_solve(boundary_condition,
                                                       heat_information,
                                                       data_building_partition_with_air_heater))

        logging.info("Finish Calculation - Finite element method")

        return data_building_partition_with_temperatures

    @staticmethod
    def define_size_matrix(data: DataFrame):
        return len(data) + 1

    @staticmethod
    def define_stiffness_matrix(data_building_partition: DataFrame, size: float):
        thickness_layer = data_building_partition.thickness.to_list()
        thermal_conductivity = data_building_partition.thermal_conductivity.to_list()

        stiffness_matrix = np.full((size, size), 0, dtype="float64")

        for i in range(size - 1):
            stiffness_matrix[i, i] += (area * thermal_conductivity[i]) / thickness_layer[i]
            stiffness_matrix[i, i + 1] += -(area * thermal_conductivity[i]) / thickness_layer[i]
            stiffness_matrix[i + 1, i] += -(area * thermal_conductivity[i]) / thickness_layer[i]
            stiffness_matrix[i + 1, i + 1] += (area * thermal_conductivity[i]) / thickness_layer[i]

        return stiffness_matrix

    @staticmethod
    def define_force_vector(data_building_partition: DataFrame, boundary_condition: dict, heat_information: dict,
                            size: float):
        thickness_layer = data_building_partition.thickness.to_list()
        thermal_conductivity = data_building_partition.thermal_conductivity.to_list()

        forces_vector = np.full(size, 0, dtype="float64")
        outdoor_condition = heat_information[ConditionsInBuilding.OUTSIDE_TEMPERATURE.value]
        if boundary_condition[BoundaryConditionDefiner.INSIDE_BC.value] == BoundaryConditionDefiner.NEUMANN.value:
            indoor_condition = heat_information[ConditionsInBuilding.INSIDE_HEATER_POWER.value]

            forces_vector[1] += outdoor_condition * area * thermal_conductivity[0] / thickness_layer[0]
            forces_vector[-1] += indoor_condition * area * thickness_layer[-1] / 2
            forces_vector[-2] += indoor_condition * area * thickness_layer[-2] / 2
        elif boundary_condition[BoundaryConditionDefiner.INSIDE_BC.value] == BoundaryConditionDefiner.DIRICHLET.value:
            indoor_condition = heat_information[ConditionsInBuilding.INSIDE_TEMPERATURE.value]

            forces_vector[1] += outdoor_condition * area * thermal_conductivity[0] / thickness_layer[0]
            forces_vector[-2] += indoor_condition * area * thermal_conductivity[-1] / thickness_layer[-1]

        return forces_vector

    @staticmethod
    def solve_equation(data_building_partition: DataFrame, boundary_condition: dict, stiffness_matrix,
                       forces_vector, size: float, heat_information: dict):
        temperatures_vector = np.full(size, 0, dtype="float64")

        temperatures_vector[0] = heat_information[ConditionsInBuilding.OUTSIDE_TEMPERATURE.value]
        if boundary_condition[BoundaryConditionDefiner.INSIDE_BC.value] == BoundaryConditionDefiner.NEUMANN.value:
            # neumann - dirichlet
            temperatures_vector[1:] = np.linalg.solve(stiffness_matrix[1:, 1:], forces_vector[1:])
            temperatures_vector = temperatures_vector[1:]

            data_building_partition['temperatures'] = [round(temp, 2) for temp in temperatures_vector]

            data_building_partition = data_building_partition[:-2]
            return data_building_partition
        elif boundary_condition[BoundaryConditionDefiner.INSIDE_BC.value] == BoundaryConditionDefiner.DIRICHLET.value:
            indoor_condition = heat_information[ConditionsInBuilding.INSIDE_TEMPERATURE.value]
            # dirichlet - dirichlet
            temperatures_vector[-1] = indoor_condition
            temperatures_vector[1:-1] = np.linalg.solve(stiffness_matrix[1:-1, 1:-1], forces_vector[1:-1])

            data_building_partition['temperatures'] = [round(temp, 2) for temp in temperatures_vector[1:]]
            return data_building_partition

    @classmethod
    def create_equation_and_solve(cls, boundary_condition, heat_information, data_building_partition):
        # http://blog.lazienkatop.pl/portfolio/grzejniki-lazienkowe-jak-dobrac-moc/
        size = cls.define_size_matrix(data=data_building_partition)

        stiffness_matrix = cls.define_stiffness_matrix(data_building_partition=data_building_partition, size=size)
        forces_vector = cls.define_force_vector(data_building_partition=data_building_partition,
                                                boundary_condition=boundary_condition,
                                                heat_information=heat_information, size=size)

        data_building_partition_with_temp = cls.solve_equation(data_building_partition=data_building_partition,
                                                               boundary_condition=boundary_condition,
                                                               stiffness_matrix=stiffness_matrix,
                                                               heat_information=heat_information,
                                                               forces_vector=forces_vector, size=size)
        return data_building_partition_with_temp

    @staticmethod
    def add_air_and_metal_heater(boundary_condition: dict, data_building_partition: DataFrame) -> DataFrame:
        """
        Within this method, information about air and a heater has been added
        if Neumann boundary conditions have been selected.
        """

        air_heater_dataframe = pd.DataFrame(air_and_heater_param)
        if boundary_condition[BoundaryConditionDefiner.INSIDE_BC.value] == BoundaryConditionDefiner.NEUMANN.value:
            logging.info(f"Adding a layer of air and a metal radiator to the data: {air_and_heater_param}")

            data_building_partition = pd.concat([data_building_partition, air_heater_dataframe], ignore_index=True)
            data_building_partition.reset_index(inplace=True, drop=True)
            return data_building_partition
        elif boundary_condition[BoundaryConditionDefiner.OUTSIDE_BC.value] == BoundaryConditionDefiner.NEUMANN.value:
            raise ValueError("The radiator should only be defined in the center of the room")
        else:
            return data_building_partition

    @staticmethod
    def thermal_resistance_method() -> DataFrame:
        logging.info("Thermal resistance calculations")
        return DataFrame
