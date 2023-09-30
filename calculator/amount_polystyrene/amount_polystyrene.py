import math


class AmountPolystyreneAndPrice:
    @staticmethod
    def calculate(wall_surface, price_square_meter, amount_package):
        package = wall_surface / amount_package
        package_rounded = math.ceil(package)

        amount_polystyrene_to_buy_square_meter = package_rounded * amount_package

        price_building = amount_polystyrene_to_buy_square_meter * price_square_meter

        return {
            "price_building": round(price_building, 2),
            "package": package_rounded,
        }
