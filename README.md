# Temperature Calculator

[![Build Status](https://github.com/rafinder1/temperature_calculator/actions/workflows/main.yaml/badge.svg)](https://github.com/rafinder1/temperature_calculator/actions/workflows/main.yaml) 

The Temperature Calculator project has been developed as part of a master's thesis in sustainable construction at the Military University of Technology in Warsaw.

## Project Description

The project primarily focuses on calculating temperatures within building partitions. Calculations are performed using finite element method equations in 1D with constant time.

### Core Features

1. **Temperature Calculation (basic_calc):**
   - To use this module, utilize the class: `TempCalculator.calculate(data_building_partition, outside_inside_thermal_data, method)`

2. **Polystyrene Selection (multivariants):**
   - The package selects the optimal type and thickness of polystyrene based on the arrangement of wall layers.
   - To use this module, use the class: `MultiVariantsCalculator.change_polystyrene(data_building_partition, outside_inside_thermal_data, polystyrene_data, method)`

3. **Polystyrene Quantity Calculation (amount_polystyrene):**
   - The package can calculate the amount of polystyrene needed for insulating a house/apartment.
   - To use this module, use the class: `AmountPolystyreneAndPrice.calculate(wall_surface, price_square_meter, amount_package)`

### GitHub Actions Integration

The project includes Continuous Integration (CI) using GitHub Actions, where tests are conducted on Ubuntu and Windows platforms, supporting Python 3.8 and 3.9 environments.

### PyPI Package

The current version of the package is a Work in Progress (WIP) and is not yet available on [PyPI](https://pypi.org/).

## Additional Information

- **Package Dockerization:** (Work in Progress)

## Versions

- **Version 0.0.4.3**



