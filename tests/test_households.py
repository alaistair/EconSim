"""Households unittest."""

import pathmagic  # noqa
import pytest
from pytest import approx
from Kuznets.household import Household
from Kuznets.settings import Settings


settings = Settings()
household = Household(settings)

def test_update_production():
    assert household.update_production(100) == 100
    assert household.update_production(0) == 0
    assert household.update_production(-100) == 0

def test_update_income_expectations():
    expected_income = household.expected_income
    inflation = 1.01
    income_tax_rate = 0.1
    assert household.update_income_expectations(
        inflation, income_tax_rate) == (
            [expected_income[-2],
             expected_income[-3],
             household.income/(1-income_tax_rate)*inflation])

    assert household.update_income_expectations(
        inflation, income_tax_rate) == (
            [expected_income[-3],
             household.income/(1-income_tax_rate)*inflation,
             household.income/(1-income_tax_rate)*inflation])

def test_update_consumption():
    """Test update_consumption.

    For now, only test that changes to household savings are correct.

    TODO: test basket updates (when multiple products are available.)

    """
    household.savings = 10
    household.expected_income = [10, 10, 10]
    spending, spending_basket = household.update_consumption()
    spending == approx(6.5)

    household.savings = 20
    household.expected_income = [20, 20, 20]
    spending, spending_basket = household.update_consumption()
    spending == approx(13)

    # Savings should not be below income.
    household.savings = 5
    household.expected_income = [10, 10, 10]
    with pytest.raises(Exception):
        household.update_consumption()

    household.savings = 15
    household.expected_income = [10, 10, 10]
    spending, spending_basket = household.update_consumption()
    spending == approx(9.75)

    household.savings = 20
    household.expected_income = [10, 10, 10]
    spending, spending_basket = household.update_consumption()
    spending == approx(13)


def test_update_financial():
    household.savings = 100
    household.update_financial(1.1) == approx(110)
    household.savings = 100
    household.update_financial(1) == approx(100)
