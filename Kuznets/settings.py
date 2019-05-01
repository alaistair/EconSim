"""Kuznets Settings class."""


class Settings():
    """
    Kuznets Settings class.

    A class to store all settings for EconSim. Settings are imported when
    initialising Kuznets. Settings here include those for the app as well as
    specific settings for the economy as well individual firms and households.

    Attributes:
        init_households: Number of households.
        init_firms: Number of firms.
        init_interest_rate: 1.02
        init_unemployment_rate: Unemployment rate.
        init_population_growth: Population growth.

        init_household_savings: Savings.
        init_MPC: Marginal propensity to consume.

        init_productivity: Output per labour input.
        init_capital_depreciation: Capital stock depreciation per cycle.

        init_govt_revenue: Government revenue.
        init_govt_expenditure: Government expenditure.
        init_govt_debt: Government debt.
        init_income_tax: Flat income tax rate.
        init_corporate_tax: Corporate tax rate.

    """

    def __init__(self):
        """Settings."""
        # App settings
        self.series_color = {'Income': 'rgb(255,255,0)',
                             'Inventory': 'rgb(25,25,112)',
                             'Savings': 'rgb(128,0,0)',
                             'Spending': 'rgb(0,102,0)',
                             }

        # Initial economy settings. Households >= firms
        self.init_households = 10
        self.init_firms = 2
        self.init_interest_rate = 1.02
        self.init_unemployment_rate = 0.2
        self.init_population_growth = 1.01

        # Initial household settings
        self.init_household_savings = 10
        self.init_MPC = 0.95

        # Initial firm settings
        self.init_productivity = 1.05  # output per labour input
        self.init_capital_depreciation = 0.03  # capital stock depn per cycle

        # Initial government settings
        self.init_govt_revenue = 0
        self.init_govt_expenditure = 0
        self.init_govt_debt = 0
        self.init_income_tax_rate = 0.10
        self.init_corporate_tax_rate = 0.30
        self.init_welfare_share = 0.6
