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

        self.income_tax_rate = settings.init_income_tax_rate
        self.corporate_tax_rate = settings.init_corporate_tax_rate

        self.welfare_share = settings.init_welfare_share

    def update_financial(self, interest_rate):
        """
        Government financial actions.

        TODO: expand govt financial decisions.
        """
        self.debt *= interest_rate
        return 1

    def income_tax(self, households):
        """
        Flat income tax.

        TODO: allow progressivity.
        """
        for h in households.values():
            self.revenue += h.income * self.income_tax_rate
            h.income *= (1-self.income_tax_rate)

    def welfare(self, income_per_capita, unemployed):
        """
        Welfare spending.

        Spending is benchmarked as a share of household income.

        TODO: make this progressive?
        """
        welfare_per_capita = self.welfare_share * income_per_capita

        if unemployed:
            for household in unemployed.values():
                household.income = welfare_per_capita
                self.expenditure += welfare_per_capita
