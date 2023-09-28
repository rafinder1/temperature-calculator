class AmountPolystyreneAndPrice:
    @staticmethod
    def calculate(wall_surface, price_square_meter, amount_package):
        price_building = wall_surface * price_square_meter

        package = wall_surface / amount_package

        return {
            "price_building": price_building,
            "package": package,
        }
