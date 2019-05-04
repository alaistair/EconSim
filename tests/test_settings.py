"""Settings unittest."""

import pathmagic  # noqa
from Kuznets.settings import Settings


def test_settings():
    """Basically test that initial settings make sense."""
    settings = Settings()

    """Economy-wide settings."""
    assert settings.households > settings.firms
    assert settings.interest_rate >= 1
    assert settings.unemployment_rate > 0
    assert settings.unemployment_rate < 1
    assert settings.population_growth > 1

    """Household settings."""
    assert settings.household_savings >= 0
    assert settings.MPC >= 0

    """Firm settings."""
    assert settings.productivity > 0
    assert settings.capital_depreciation >= 0

    """Government settings."""
    assert settings.govt_revenue >= 0
    assert settings.govt_expenditure >= 0
    assert settings.govt_debt >= 0
    assert settings.income_tax_rate >= 0
    assert settings.corporate_tax_rate >= 0
    assert settings.welfare_share >= 0
    assert settings.welfare_share <= 1
