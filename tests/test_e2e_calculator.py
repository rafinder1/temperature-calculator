import unittest

from main.calculator import TempCalculator


class MainTestCase(unittest.TestCase):
    def test_temperature_calculator(self):
        expected = "This is Temperature calculator - package"
        txt = TempCalculator.calculate()
        self.assertEqual(expected, txt)
