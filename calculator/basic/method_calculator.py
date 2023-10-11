import numpy as np
import pandas as pd
from enum import Enum
from calculator.basic.config import BoundaryConditionName, ConditionsInBuilding, air_and_heater_param


class MethodCalculator(Enum):
    FINITE_ELEMENT_METHOD = 'finite_element_method'
    THERMAL_RESISTANCE_METHOD = 'thermal_resistance_method'

    @classmethod
    def calculate_by_method(cls, method: str, data_building_partition, heat_information, boundary_condition):
        if method == cls.FINITE_ELEMENT_METHOD.value:
            return cls.finite_element_method(data_building_partition, heat_information, boundary_condition)
        elif method == cls.THERMAL_RESISTANCE_METHOD.value:
            return cls.thermal_resistance_method()
        else:
            raise ValueError("This method does not exist")

    @staticmethod
    def finite_element_method(data_building_partition, heat_information, boundary_condition):
        """
        The finite element method in the 1D dimension was used to calculate the heat
        """

        data_building_partition_with_air_heater = MethodCalculator.add_air_and_metal_heater(boundary_condition,
                                                                                            data_building_partition)
        data_building_partition_with_temperatures = (
            MethodCalculator.create_equation_and_solve(boundary_condition,
                                                       heat_information,
                                                       data_building_partition_with_air_heater))

        return data_building_partition_with_temperatures

    @staticmethod
    def create_equation_and_solve(boundary_condition, heat_information, data_building_partition):
        thickness_layer = data_building_partition.thickness.to_list()
        thermal_conductivity = data_building_partition.thermal_conductivity.to_list()

        size = len(thermal_conductivity) + 1
        stiffness_matrix = np.full((size, size), 0, dtype="float64")
        forces_vector = np.full(size, 0, dtype="float64")
        temperatures_vector = np.full(size, 0, dtype="float64")

        # http://blog.lazienkatop.pl/portfolio/grzejniki-lazienkowe-jak-dobrac-moc/
        area = 25
        for i in range(size - 1):
            stiffness_matrix[i, i] += (area * thermal_conductivity[i]) / thickness_layer[i]
            stiffness_matrix[i, i + 1] += -(area * thermal_conductivity[i]) / thickness_layer[i]
            stiffness_matrix[i + 1, i] += -(area * thermal_conductivity[i]) / thickness_layer[i]
            stiffness_matrix[i + 1, i + 1] += (area * thermal_conductivity[i]) / thickness_layer[i]
        indoor_condition, outdoor_condition = MethodCalculator.define_condition_building(boundary_condition,
                                                                                         heat_information)
        temperatures_vector[0] = outdoor_condition

        if boundary_condition[BoundaryConditionName.inside.value] == BoundaryConditionName.neumann.value and \
                boundary_condition[BoundaryConditionName.outside.value] == BoundaryConditionName.dirichlet.value:
            # neumann - dirichlet
            forces_vector[1] += outdoor_condition * area * thermal_conductivity[0] / thickness_layer[0]
            forces_vector[-1] += indoor_condition * area * thickness_layer[-1] / 2
            forces_vector[-2] += indoor_condition * area * thickness_layer[-2] / 2

            temperatures_vector[1:] = np.linalg.solve(stiffness_matrix[1:, 1:], forces_vector[1:])
            temperatures_vector = temperatures_vector[1:]

            data_building_partition['temperatures'] = [round(temp, 2) for temp in temperatures_vector]

            data_building_partition = data_building_partition[:-2]

        elif boundary_condition[BoundaryConditionName.outside.value] == BoundaryConditionName.dirichlet.value and \
                boundary_condition[BoundaryConditionName.inside.value] == BoundaryConditionName.dirichlet.value:
            # dirichlet - dirichlet
            temperatures_vector[-1] = indoor_condition
            forces_vector[1] += outdoor_condition * area * thermal_conductivity[0] / thickness_layer[0]
            forces_vector[-2] += indoor_condition * area * thermal_conductivity[-1] / thickness_layer[-1]
            temperatures_vector[1:-1] = np.linalg.solve(stiffness_matrix[1:-1, 1:-1], forces_vector[1:-1])

            data_building_partition['temperatures'] = [round(temp, 2) for temp in temperatures_vector[1:]]

        else:
            print("Different Boundary Condition no calculate")

        return data_building_partition

    @staticmethod
    def define_condition_building(boundary_condition, heat_information):
        if boundary_condition[BoundaryConditionName.inside.value] == BoundaryConditionName.dirichlet.value:
            indoor_condition = heat_information[ConditionsInBuilding.inside_temperature.value]
        else:
            indoor_condition = heat_information[ConditionsInBuilding.inside_heater_power.value]
        if boundary_condition[BoundaryConditionName.outside.value] == BoundaryConditionName.dirichlet.value:
            outdoor_condition = heat_information[ConditionsInBuilding.outside_temperature.value]
        else:
            outdoor_condition = heat_information[ConditionsInBuilding.outside_temperature.value]
        return indoor_condition, outdoor_condition

    @staticmethod
    def add_air_and_metal_heater(boundary_condition, data_building_partition):
        """
        Within this method, information about air and a heater has been added
        if Neumann boundary conditions have been selected.
        """

        air_heater_dataframe = pd.DataFrame(air_and_heater_param)

        if boundary_condition[BoundaryConditionName.inside.value] == BoundaryConditionName.neumann.value:
            data_building_partition = pd.concat([data_building_partition, air_heater_dataframe], ignore_index=True)

        elif boundary_condition[BoundaryConditionName.outside.value] == BoundaryConditionName.neumann.value:
            data_building_partition = pd.concat([air_heater_dataframe, data_building_partition], ignore_index=True)
        else:
            pass

        data_building_partition.reset_index(inplace=True, drop=True)

        return data_building_partition

    @staticmethod
    def thermal_resistance_method():
        print("Calling thermal_resistance_method")
