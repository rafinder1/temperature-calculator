import unittest
from calculator.amount_polystyrene.amount_polystyrene import AmountPolystyreneAndPrice


class MainTestCase(unittest.TestCase):
    def test_amount_price_polystyrene_calculator(self):
        # when
        wall_surface = 100
        price_square_meter = 27.03
        amount_package = 2

        # given
        tested_data = AmountPolystyreneAndPrice.calculate(wall_surface=wall_surface,
                                                          price_square_meter=price_square_meter,
                                                          amount_package=amount_package)

        # then
        expected = {'price_building': 2703.0, 'package': 50.0}

        self.assertEqual(tested_data, expected)
