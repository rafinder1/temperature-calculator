"""
Calculator for Polystyrene Amount and Price

This module contains a class for calculating the amount of polystyrene required and its price
based on given data, along with supporting utility methods for calculations.

The main class, `AmountPolystyreneAndPrice`, provides methods to calculate the number of polystyrene
packages needed and the total price based on parameters such as wall surface area, price per square
meter, and the amount of polystyrene in one package.

Additionally, this module includes utility methods for rounding numbers and calculating package
counts.
"""
import logging
import math
import sys

from calculator.config import GLOBAL_LOGGING_LEVEL

logging.basicConfig(stream=sys.stdout, level=GLOBAL_LOGGING_LEVEL)


class AmountPolystyreneAndPrice:
    """
    A class for calculating the amount of polystyrene required and its price.

    This class provides methods for calculating the number of polystyrene packages needed to cover a
    wall surface and the total price of polystyrene based on the given data.
    """

    @classmethod
    def calculate(cls, wall_surface: float, price_square_meter: float,
                  amount_polystyrene_in_one_package: float) -> dict:
        """
        Calculate the amount of polystyrene required and its price based on the given data.

        This method takes in the wall surface area, price per square meter of polystyrene,
        and the amount of polystyrene in one package, and calculates the required package count
        and the total price.

        :return: A dictionary containing the calculated results:
            - 'price_building': The total price of polystyrene for the given wall surface.
            - 'package': The number of packages of polystyrene required, rounded up to the
            nearest whole package.
        """
        logging.info("Calculation of the amount of polystyrene and its price based on the data: \n"
                     "1. Wall surface - %s m2,\n"
                     "2. Price per square meter %s zł,\n"
                     "3. amount in one package %s m2.",
                     wall_surface, price_square_meter, amount_polystyrene_in_one_package)
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
        """
        Calculate the total price of polystyrene for a given number of packages.

        This method computes the total price of polystyrene insulation based on the provided
        amount of polystyrene in one
        package, the number of packages needed, and the price per square meter of polystyrene.

        :raises ValueError: If any of the input values are non-positive (<= 0), a ValueError is
        raised with an appropriate message.
        """
        logging.info("Calculate Price Polystyrene")
        try:
            if price_polystyrene_per_square_meter <= 0:
                logging.warning("The price per square meter must be more than zero")
                raise ValueError("The price per square meter is <= 0")
            if amount_polystyrene_in_one_package <= 0:
                logging.warning("The amount of Polystyrene in the package must be more than zero")
                raise ValueError("The amount of Polystyrene is <= 0")
            if package <= 0:
                logging.warning("The amount package must be more than zero")
                raise ValueError("The amount package is <= 0")

            amount_polystyrene_to_buy = cls.calculate_amount_polystyrene_to_buy(
                amount_polystyrene_in_one_package=amount_polystyrene_in_one_package,
                package=package)
            return round(amount_polystyrene_to_buy * price_polystyrene_per_square_meter, 2)
        except ValueError as error:
            print(f"An error occurred: {error}")
            return None

    @classmethod
    def calculate_amount_polystyrene_to_buy(cls, amount_polystyrene_in_one_package: float,
                                            package: int) -> float:
        """
        Calculate the total amount of polystyrene to buy based on the number of packages required.

        This method computes the total amount of polystyrene insulation to purchase based on the
        amount of polystyrene in one package and the number of packages needed.

        :return: The total amount of polystyrene to buy in square meters.
        :rtype: float
        """
        return package * amount_polystyrene_in_one_package

    @staticmethod
    def calculate_amount_package(amount_package: float, wall_surface: float) -> float:
        """
        Calculate the number of packages of polystyrene required for a given wall surface area.

        This method computes the number of packages of polystyrene insulation needed to cover a
        specified wall surface area.

        :return: The number of packages of polystyrene required to cover the wall surface.
        :rtype: float
        """
        return wall_surface / amount_package

    @staticmethod
    def round_up(param: float) -> int:
        """
        Round a floating-point number up to the nearest integer.

        This method takes a floating-point number as input and rounds it up to the nearest
        integer using the `math.ceil` function.

        :return: The rounded-up integer value.
        :rtype: int
        """
        return math.ceil(param)

    @classmethod
    def calculate_amount_package_and_round_up(cls, amount_polystyrene_in_one_package: float,
                                              wall_surface: float) -> int:
        """
        Calculate the number of packages of polystyrene required for a wall surface and round up
        to the nearest whole package.

        This method computes the number of packages of polystyrene insulation needed to cover a
        specified wall surface area and rounds the result up to the nearest whole package.

        :return: The number of packages of polystyrene required, rounded up to the nearest whole
        package.
        :rtype: int
        """
        logging.info("Calculate Amount Package")

        try:
            if amount_polystyrene_in_one_package <= 0:
                logging.warning("The amount of Polystyrene in the package must be more than zero")
                raise ValueError("The amount of Polystyrene is <= 0")
            if wall_surface <= 0:
                logging.warning("Wall surface must be more than zero")
                raise ValueError("Wall surface is <= 0")
            package = cls.calculate_amount_package(amount_package=amount_polystyrene_in_one_package,
                                                   wall_surface=wall_surface)
            return cls.round_up(param=package)

        except ValueError as error:
            print(f"An error occurred: {error}")
            return None
