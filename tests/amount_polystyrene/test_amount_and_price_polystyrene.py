import pytest

from calculator.amount_polystyrene.amount_polystyrene import AmountPolystyreneAndPrice

amount_package = [
    (10, 100, 10),
    (15, 50, 4),
    (-1, 100, None),
    (10, -50, None)
]


@pytest.mark.parametrize("amount_polystyrene_in_one_package, wall_surface, expected_amount_package", amount_package)
def test_calculate_amount_package(amount_polystyrene_in_one_package, wall_surface, expected_amount_package):
    package_rounded = AmountPolystyreneAndPrice.calculate_amount_package_and_round_up(
        amount_polystyrene_in_one_package=amount_polystyrene_in_one_package,
        wall_surface=wall_surface)
    assert (package_rounded == expected_amount_package)
