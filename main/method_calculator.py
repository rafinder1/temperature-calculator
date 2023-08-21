import numpy as np


class MethodCalculator:
    @staticmethod
    def select_calculation_method(method):
        return getattr(MethodCalculator, method.value)

    @staticmethod
    def finite_element_method(data_building_partition, heat_information, boundary_condition):
        thickness_layer = data_building_partition.thickness.to_list()
        type_layer = data_building_partition.type_layer
        thermal_conductivity = data_building_partition.thermal_conductivity.to_list()

        if boundary_condition['inside_boundary_condition'] == 'neumann':
            thermal_conductivity.extend([0.025, 50])
            thickness_layer.extend([0.1, 0.1])

        size = len(thermal_conductivity) + 1
        A = np.full((size, size), 0, dtype="float64")  # stiffness matrix
        B = np.full(size, 0, dtype="float64")  # forces vector
        Ts = np.full(size, 0, dtype="float64")  # temperatures vector

        area = 5
        for i in range(size - 1):
            A[i, i] += (area * thermal_conductivity[i]) / thickness_layer[i]
            A[i, i + 1] += -(area * thermal_conductivity[i]) / thickness_layer[i]
            A[i + 1, i] += -(area * thermal_conductivity[i]) / thickness_layer[i]
            A[i + 1, i + 1] += (area * thermal_conductivity[i]) / thickness_layer[i]

        temp_outdoor = heat_information['main']['outside_temperature']
        temp_or_power = heat_information['main']['inside_heater_power']
        Ts[0] = temp_outdoor
        B[1] += temp_outdoor * area * thermal_conductivity[0] / thickness_layer[0]
        B[-1] += temp_or_power * area * thickness_layer[-1] / 2
        B[-2] += temp_or_power * area * thickness_layer[-2] / 2
        Ts[1:] = np.linalg.solve(A[1:, 1:], B[1:])
        thermal_conductivity = thermal_conductivity[:len(thermal_conductivity) - 2]
        thickness_layer = thickness_layer[:len(thickness_layer) - 2]
        Ts = Ts[:len(Ts) - 2]

        return Ts

    @staticmethod
    def thermal_resistance_method():
        print("Calling thermal_resistance_method")
