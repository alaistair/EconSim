"""Kuznets Government class."""


class Government():
    """
    Kuznets Government class.

    Each economy instantiates one government only.

    Args:
        settings: Initial government settings.

    Attributes:
        revenue: Init at 0.
        expenditure: Init at 0.
        debt: Init at 0.

        income_tax: Flat tax (for now). Init at 10%.
        corporate_tax: Init at 10%.

    """

    def __init__(self, settings):
        """Init Government using Settings class."""
        self.revenue = settings.init_govt_revenue
        self.expenditure = settings.init_govt_expenditure
        self.debt = settings.init_govt_debt

        self.income_tax = settings.init_income_tax
        self.corporate_tax = settings.init_corporate_tax

    def govt_financial(self, interest_rate):
        """
        Government financial actions.

        TODO: expand govt financial decisions.
        """
        self.debt *= interest_rate
        return 1
