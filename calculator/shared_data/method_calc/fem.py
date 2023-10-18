import logging

import numpy as np
import pandas as pd
from numpy import ndarray
from pandas import DataFrame

from calculator.shared_data.boundary_condition_definer import BoundaryConditionDefiner
from calculator.shared_data.method_calc.config import area, air_heater_dataframe
from calculator.shared_data.outside_inside_thermal_data import OutsideInsideThermalData


class FEM:
    @classmethod
    def calculate(cls, data_building_partition: DataFrame,
                  outside_inside_thermal_data: OutsideInsideThermalData,
                  boundary_condition: dict):
        """
        The finite element method in the 1D dimension was used to calculate the heat
        """
        logging.info("Finite element calculations")

        data_building_partition_with_air_heater = cls.add_air_and_metal_heater(
            boundary_condition=boundary_condition,
            data_building_partition=data_building_partition)

        data_building_partition_with_temperatures = (
            cls.create_equation_and_solve(boundary_condition,
                                          outside_inside_thermal_data,
                                          data_building_partition_with_air_heater))

        logging.info("Finish Calculation - Finite element method")

        return data_building_partition_with_temperatures

    @staticmethod
    def define_size_matrix(data: DataFrame):
        return len(data) + 1

    @classmethod
    def define_stiffness_matrix(cls, data_building_partition: DataFrame, size: float):

        stiffness_matrix = cls.get_stiffness_matrix_with_zero(size)

        stiffness_matrix_with_data = cls.add_data_to_stiffness_matrix(
            size=size, stiffness_matrix=stiffness_matrix,
            data_building_partition=data_building_partition)

        return stiffness_matrix_with_data

    @staticmethod
    def add_data_to_stiffness_matrix(size: int, stiffness_matrix: ndarray,
                                     data_building_partition: DataFrame) -> ndarray:
        thickness_layer = data_building_partition.thickness.to_list()
        thermal_conductivity = data_building_partition.thermal_conductivity.to_list()
        for i in range(size - 1):
            stiffness_matrix[i, i] += (area * thermal_conductivity[i]) / thickness_layer[i]
            stiffness_matrix[i, i + 1] += -(area * thermal_conductivity[i]) / thickness_layer[i]
            stiffness_matrix[i + 1, i] += -(area * thermal_conductivity[i]) / thickness_layer[i]
            stiffness_matrix[i + 1, i + 1] += (area * thermal_conductivity[i]) / thickness_layer[i]

        return stiffness_matrix

    @staticmethod
    def get_stiffness_matrix_with_zero(size: int) -> ndarray:
        return np.full((size, size), 0, dtype="float64")

    @staticmethod
    def get_vector_with_zero(size: int) -> ndarray:
        return np.full(size, 0, dtype="float64")

    @classmethod
    def define_force_vector(cls, data_building_partition: DataFrame, boundary_condition: dict,
                            outside_inside_thermal_data: OutsideInsideThermalData,
                            size: float):

        forces_vector = cls.get_vector_with_zero(size=size)

        forces_vector_with_data = cls.add_data_to_forces_vector(boundary_condition,
                                                                data_building_partition,
                                                                forces_vector,
                                                                outside_inside_thermal_data)

        return forces_vector_with_data

    @classmethod
    def add_data_to_forces_vector(cls, boundary_condition, data_building_partition, forces_vector,
                                  outside_inside_thermal_data):

        if boundary_condition['inside_bc'] == BoundaryConditionDefiner.NEUMANN.value:
            cls.update_fv_for_neumann_bc(forces_vector, data_building_partition,
                                         outside_inside_thermal_data)
        elif boundary_condition["outside_bc"] == BoundaryConditionDefiner.DIRICHLET.value:

            cls.update_fv_for_dirichlet_bc(forces_vector, data_building_partition,
                                           outside_inside_thermal_data)

        return forces_vector

    @classmethod
    def update_fv_for_dirichlet_bc(cls, forces_vector: ndarray, data_building_partition: DataFrame,
                                   outside_inside_thermal_data: OutsideInsideThermalData, ):

        outdoor_condition = outside_inside_thermal_data.OUTSIDE_TEMPERATURE
        thermal_conductivity = data_building_partition.thermal_conductivity.to_list()
        thickness_layer = data_building_partition.thickness.to_list()
        indoor_condition = outside_inside_thermal_data.INSIDE_TEMPERATURE
        forces_vector[1] += cls.update_fv_from_outdoor_condition(
            outdoor_condition, thermal_conductivity, thickness_layer)
        forces_vector[-2] += indoor_condition * area * thermal_conductivity[-1] / thickness_layer[
            -1]

    @classmethod
    def update_fv_for_neumann_bc(cls, forces_vector: ndarray, data_building_partition: DataFrame,
                                 outside_inside_thermal_data: OutsideInsideThermalData,
                                 ):
        outdoor_condition = outside_inside_thermal_data.OUTSIDE_TEMPERATURE
        thermal_conductivity = data_building_partition.thermal_conductivity.to_list()
        thickness_layer = data_building_partition.thickness.to_list()

        indoor_condition = outside_inside_thermal_data.INSIDE_HEATER_POWER
        forces_vector[1] += cls.update_fv_from_outdoor_condition(
            outdoor_condition, thermal_conductivity, thickness_layer)
        forces_vector[-1] += indoor_condition * area * thickness_layer[-1] / 2
        forces_vector[-2] += indoor_condition * area * thickness_layer[-2] / 2

    @staticmethod
    def update_fv_from_outdoor_condition(outdoor_condition: float, thermal_conductivity: float,
                                         thickness_layer: float) -> float:
        return outdoor_condition * area * thermal_conductivity[0] / thickness_layer[0]

    @classmethod
    def solve_equation(cls, data_building_partition: DataFrame, boundary_condition: dict,
                       stiffness_matrix,
                       forces_vector, size: float,
                       outside_inside_thermal_data: OutsideInsideThermalData):
        temperatures_vector = cls.get_vector_with_zero(size=size)

        temperatures_vector[0] = outside_inside_thermal_data.OUTSIDE_TEMPERATURE
        if boundary_condition['inside_bc'] == BoundaryConditionDefiner.NEUMANN.value:
            # neumann - dirichlet
            temperatures_vector[1:] = np.linalg.solve(stiffness_matrix[1:, 1:], forces_vector[1:])
            temperatures_vector = temperatures_vector[1:]

            data_building_partition['temperatures'] = [round(temp, 2) for temp in
                                                       temperatures_vector]

            data_building_partition = data_building_partition[:-2]
            return data_building_partition
        elif boundary_condition["outside_bc"] == BoundaryConditionDefiner.DIRICHLET.value:
            indoor_condition = outside_inside_thermal_data.INSIDE_TEMPERATURE
            # dirichlet - dirichlet
            temperatures_vector[-1] = indoor_condition
            temperatures_vector[1:-1] = np.linalg.solve(stiffness_matrix[1:-1, 1:-1],
                                                        forces_vector[1:-1])

            data_building_partition['temperatures'] = [round(temp, 2) for temp in
                                                       temperatures_vector[1:]]
            return data_building_partition

    @classmethod
    def create_equation_and_solve(cls, boundary_condition, outside_inside_thermal_data,
                                  data_building_partition):
        # http://blog.lazienkatop.pl/portfolio/grzejniki-lazienkowe-jak-dobrac-moc/
        size = cls.define_size_matrix(data=data_building_partition)

        stiffness_matrix = cls.define_stiffness_matrix(
            data_building_partition=data_building_partition, size=size
        )

        forces_vector = cls.define_force_vector(
            data_building_partition=data_building_partition,
            boundary_condition=boundary_condition,
            outside_inside_thermal_data=outside_inside_thermal_data,
            size=size
        )

        data_building_partition_with_temp = cls.solve_equation(
            data_building_partition=data_building_partition,
            boundary_condition=boundary_condition,
            outside_inside_thermal_data=outside_inside_thermal_data,
            forces_vector=forces_vector, stiffness_matrix=stiffness_matrix, size=size)

        return data_building_partition_with_temp

    @staticmethod
    def add_air_and_metal_heater(boundary_condition: dict,
                                 data_building_partition: DataFrame) -> DataFrame:
        """
        Within this method, information about air and a heater has been added
        if Neumann boundary conditions have been selected.
        """

        if boundary_condition["inside_bc"] == BoundaryConditionDefiner.NEUMANN.value:
            logging.info(
                f"Adding a layer of air and a metal radiator to the data: {air_heater_dataframe}")

            data_building_partition = pd.concat([data_building_partition, air_heater_dataframe],
                                                ignore_index=True)
            data_building_partition.reset_index(inplace=True, drop=True)
            return data_building_partition
        elif boundary_condition["outside_bc"] == BoundaryConditionDefiner.NEUMANN.value:
            raise ValueError("The radiator should only be defined in the center of the room")
        else:
            return data_building_partition
