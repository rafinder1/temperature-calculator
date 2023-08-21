class MethodCalculator:
    @staticmethod
    def select_calculation_method(method):
        return getattr(MethodCalculator, method.value)

    @staticmethod
    def finite_element_method(data_building_partition, heat_information, boundary_condition):
        print("Calling finite_element_method")
        return "FEM"

    @staticmethod
    def thermal_resistance_method():
        print("Calling thermal_resistance_method")
