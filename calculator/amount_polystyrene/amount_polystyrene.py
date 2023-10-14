import logging
import math
import sys

from calculator.config import GLOBAL_LOGGING_LEVEL

logging.basicConfig(stream=sys.stdout, level=GLOBAL_LOGGING_LEVEL)


class AmountPolystyreneAndPrice:
    @classmethod
    def calculate(cls, wall_surface: float, price_square_meter: float,
                  amount_polystyrene_in_one_package: float) -> dict:
        logging.info("Calculation of the amount of polystyrene and its price based on the data: \n"
                     f"1. Wall surface - {wall_surface} m2,\n"
                     f"2. Price per square meter {price_square_meter} zł,\n"
                     f"3. amount in one package {amount_polystyrene_in_one_package} m2.")
        package_rounded = cls.calculate_amount_package_and_round_up(
            amount_polystyrene_in_one_package=amount_polystyrene_in_one_package,
            wall_surface=wall_surface)

        price_polystyrene = cls.calculate_price_polystyrene(
            amount_polystyrene_in_one_package=amount_polystyrene_in_one_package,
            package=package_rounded,
            price_polystyrene_per_square_meter=price_square_meter)
        logging.info("Finish calculate")

        return {
            "price_building": price_polystyrene,
            "package": package_rounded,
        }

    @classmethod
    def calculate_price_polystyrene(cls, amount_polystyrene_in_one_package: float, package: int,
                                    price_polystyrene_per_square_meter: float) -> float:
        logging.info("Calculate Price Polystyrene")
        try:
            if price_polystyrene_per_square_meter <= 0:
                raise ValueError("the price per square meter must be  more than zero")
            amount_polystyrene_to_buy = cls.calculate_amount_polystyrene_to_buy(
                amount_polystyrene_in_one_package=amount_polystyrene_in_one_package,
                package=package)
            return round(amount_polystyrene_to_buy * price_polystyrene_per_square_meter, 2)
        except ValueError as e:
            print(f"An error occurred: {e}")

    @classmethod
    def calculate_amount_polystyrene_to_buy(cls, amount_polystyrene_in_one_package: float, package: int) -> float:
        return package * amount_polystyrene_in_one_package

    @staticmethod
    def calculate_amount_package(amount_package: float, wall_surface: float) -> float:
        return wall_surface / amount_package

    @staticmethod
    def round_up(param: float) -> int:
        return math.ceil(param)

    @classmethod
    def calculate_amount_package_and_round_up(cls, amount_polystyrene_in_one_package: float,
                                              wall_surface: float) -> int:
        logging.info("Calculate Amount Package")

        try:
            if amount_polystyrene_in_one_package <= 0:
                raise ValueError("The amount of Polystyrene in the package must be more than zero")
            if wall_surface <= 0:
                raise ValueError("Wall surface must be more than zero")
            package = cls.calculate_amount_package(amount_package=amount_polystyrene_in_one_package,
                                                   wall_surface=wall_surface)
            return cls.round_up(param=package)

        except ValueError as e:
            print(f"An error occurred: {e}")

