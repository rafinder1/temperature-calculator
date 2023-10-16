import pytest

from calculator.amount_polystyrene.amount_polystyrene import AmountPolystyreneAndPrice

amount_package = [
    (10, 100, 10),
    (15, 50, 4),
    (-1, 100, None),
    (10, -50, None)
]


@pytest.mark.parametrize("amount_polystyrene_in_one_package, wall_surface, expected_amount_package",
                         amount_package)
def test_calculate_amount_package(amount_polystyrene_in_one_package, wall_surface,
                                  expected_amount_package):
    package_rounded = AmountPolystyreneAndPrice.calculate_amount_package_and_round_up(
        amount_polystyrene_in_one_package=amount_polystyrene_in_one_package,
        wall_surface=wall_surface)
    assert (package_rounded == expected_amount_package)


price_polystyrene = [
    (6.35, 52, 10, 3302.0),
    (77.86, 101, 1, 7863.86),
    (-2.88, 100, 15, None),
    (10, -10, 6, None),
    (10, 10, -6, None)
]


@pytest.mark.parametrize("polystyrene_in_one_package, package, price_sm, expected_price",
                         price_polystyrene)
def test_calculate_price_polystyrene(polystyrene_in_one_package, package, price_sm, expected_price):
    price_calc = AmountPolystyreneAndPrice.calculate_price_polystyrene(
        amount_polystyrene_in_one_package=polystyrene_in_one_package,
        package=package,
        price_polystyrene_per_square_meter=price_sm)
    assert (price_calc == expected_price)
