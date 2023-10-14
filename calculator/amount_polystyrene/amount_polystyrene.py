import math


class AmountPolystyreneAndPrice:
    @classmethod
    def calculate(cls, wall_surface, price_square_meter, amount_package):
        package_rounded = cls.calculate_amount_package_and_round_up(amount_package=amount_package,
                                                                    wall_surface=wall_surface)

        price_polystyrene = cls.calculate_price_polystyrene(amount_package, package_rounded, price_square_meter)

        return {
            "price_building": price_polystyrene,
            "package": package_rounded,
        }

    @classmethod
    def calculate_price_polystyrene(cls, amount_package: float, package: int,
                                    price_polystyrene_per_square_meter: float) -> float:
        amount_polystyrene_to_buy = cls.calculate_amount_polystyrene_to_buy(amount_package=amount_package,
                                                                            package=package)
        return round(amount_polystyrene_to_buy * price_polystyrene_per_square_meter, 2)

    @classmethod
    def calculate_amount_polystyrene_to_buy(cls, amount_package: float, package: int) -> float:
        return package * amount_package

    @staticmethod
    def calculate_amount_package(amount_package: float, wall_surface: float) -> float:
        return wall_surface / amount_package

    @staticmethod
    def round_up(param: float) -> int:
        return math.ceil(param)

    @classmethod
    def calculate_amount_package_and_round_up(cls, amount_package: float, wall_surface: float) -> int:
        package = cls.calculate_amount_package(amount_package=amount_package, wall_surface=wall_surface)

        return cls.round_up(param=package)
