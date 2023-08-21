from enum import Enum


class MethodName(Enum):
    finite_element_method = "finite_element_method"


class BoundaryConditionName(Enum):
    neumann = "neumann"
    dirichlet = "dirichlet"
