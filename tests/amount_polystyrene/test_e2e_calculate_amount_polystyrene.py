import unittest

from calculator.amount_polystyrene.amount_polystyrene import AmountPolystyreneAndPrice


class MainTestCase(unittest.TestCase):
    def test_amount_price_polystyrene_calculator(self):
        # when
        wall_surface = 100.0
        price_square_meter = 35.12
        amount_package = 2.8

        # given
        tested_data = AmountPolystyreneAndPrice.calculate(
            wall_surface=wall_surface, price_square_meter=price_square_meter,
            amount_polystyrene_in_one_package=amount_package)

        # then
        expected = {'price_building': 3540.1, 'package': 36}

        self.assertEqual(tested_data, expected)
