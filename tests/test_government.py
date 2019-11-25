"""Government class unittest."""

import pathmagic  # noqa
import pytest
from pytest import approx
from Kuznets.government import Government
from Kuznets.household import Household
from Kuznets.settings import Settings

settings = Settings()
government = Government(settings)


def test_init_government():
    """Test initial Government settings make sense."""
    assert government.revenue == settings.govt_revenue

def test_update_financial():
    #assert household.update_production(100) == 100
    pass

def test_income_tax():
    pass
