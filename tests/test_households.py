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
    # Spending == average expected income if savings <= last income and
    # incomes rising.
    household.savings = 0
    household.expected_income = [5, 10, 15]
    spending, spending_basket = household.update_consumption()
    assert spending == 10

    household.savings = 10
    household.expected_income = [10, 10, 10]
    spending, spending_basket = household.update_consumption()
    assert spending == 10

    # Spending == last income if savings <= last income and incomes falling.
    household.savings = 0
    household.expected_income = [15, 10, 5]
    spending, spending_basket = household.update_consumption()
    assert spending == 5

    household.savings = 11
    household.expected_income = [10, 10, 10]
    spending, spending_basket = household.update_consumption()
    assert spending == 8

    household.savings = 13
    household.expected_income = [10, 10, 10]
    spending, spending_basket = household.update_consumption()
    assert spending == 9.5

    household.savings = 15
    household.expected_income = [10, 10, 10]
    spending, spending_basket = household.update_consumption()
    assert spending == 9.5

    household.savings = 17
    household.expected_income = [10, 10, 10]
    spending, spending_basket = household.update_consumption()
    assert spending == 10.4

@pytest.mark.parametrize(
    "savings, expected",
    [(11, 8)])
def test_update_consumption2():
    household.savings = savings
    spending, spending_basket = household.update_consumption()

    assert household.spending == expected

def test_update_financial():
    household.savings = 100
    household.update_financial(1.1) == approx(110)
    household.savings = 100
    household.update_financial(1) == approx(100)
