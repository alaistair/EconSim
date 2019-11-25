"""Firm class unittest."""

import pathmagic  # noqa
import pytest
from pytest import approx
from Kuznets.firm import Firm
from Kuznets.settings import Settings

settings = Settings()
firm = Firm(settings)


def test_init_firm():
    """Test initial Firm settings make sense."""
    assert firm.productivity == settings.firm_productivity
    assert firm.capital_investment == 0
    assert firm.capital_stock >= 0
    assert firm.capital_share >= 0
    assert firm.human_capital == 0
    assert firm.human_capital_share >= 0
    assert firm.labour_share >= 0

    assert firm.interest_rate >= 0
    assert firm.debt >= 0
    assert firm.capital_depreciation >= 0

    assert firm.expected_production >= 0
    assert firm.production == 0
    assert firm.product_price > 0
    assert firm.inventory == 0
    assert firm.revenue == 0
    assert firm.labour_cost == 0
    assert firm.marginal_cost == 0
    assert firm.profit == 0

    assert not firm.workers
    assert not firm.owners

#def test_update_expected_production():
