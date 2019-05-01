"""Kuznets Households class."""

import numpy as np
import random


class Household():
    """
    Kuznets Households class.

    Each household earns income, spends, and saves. Each household is
    initialised with random human capital, which affects their expected income.
    Future development include life cycle (aging, family formation) and asset
    markets.

    Args:
        settings: Initial household settings.

    Attributes:
        people: Does nothing so far.
        age: Does nothing so far.
        human_capital: Randomly initialised, normally distributed at 1. Human
            capital cannot go below zero (for now), ie no zero marginal
            product workers. In periods of employment it accrues while in
            periods of unemployment it depreciates.

        life_stage: 'U' = unemployed, 'E' = employed, 'S' = studying, 'R' =
            retired.
        expected_income: Pretax expected income. Average of past three incomes.
        income: Income from working for one cycle.

        MPC: Marginal propensity to consume.
        spending: Spending for one cycle.
        spending_basket: List of products along with willing bid prices and the
            proportion of total household spending on that product.
        savings: Stock of savings.

    """

    def __init__(self, settings):
        """Init Household with Settings."""
        self.people = 1
        self.age = 18
        self.human_capital = np.random.normal(1, 0.25)
        if self.human_capital < 0:
            self.human_capital = 0

        self.life_stage = 'U'
        self.expected_income = [10*self.human_capital,
                                10*self.human_capital,
                                10*self.human_capital]
        self.income = 0

        self.MPC = settings.init_MPC
        self.spending = 0
        self.spending_basket = [{'Name': 'A',
                                 'Price': 1 + (random.random() - 0.5) * 0.1,
                                 'Proportion': 1}]
        self.savings = settings.init_household_savings

    def update_production(self, income):
        """Update income."""
        income = 0 if income < 0 else income
        self.income = income
        return self.income

    def update_income_expectations(self, inflation, income_tax_rate):
        """
        Update expected income given current income.

        If household is employed, append current income and increase human
        capital endowment slightly to account for increase in on-the-job
        knowledge.

        If unemployed, also append current income (welfare) and decrease
        human capital to reflect deterioration in skills.

        Args:
            inflation (float): Inflation rate (1.05 === 5%).
            income_tax_rate (float): Flat tax.

        Returns:
            expected_income ([float]): List of past three incomes.

        """
        if inflation < 1:
            inflation = 1  # sticky wage expectations

        self.expected_income.pop(0)
        if self.life_stage == 'E':
            self.expected_income.append(
                self.income/(1 - income_tax_rate) * (1 + inflation/100))
            self.human_capital *= 1.001
        elif self.life_stage == 'U':
            self.expected_income.append(self.income)
            self.human_capital *= 0.995

        return self.expected_income

    def update_consumption(self):
        """Decide spending/saving mix for this cycle.

        When this is called, current income (expected_income[-1]) should
        already have been added to savings. Hence if savings are equal to
        current income, the household has no savings. Moreover if the latest
        income is below expectations, current income likely is falling. In
        these cases the household will not save (permanent income hypothesis
        assumption).

        However if savings are above current income then we adjust the MPC in
        line with the stock of savings.

        Returns:
            spending_basket: This reflects that this function will eventually
                incorporate decisions on the spending mix as well as the total
                sum of spending.

        """
        if self.savings <= self.expected_income[-1]:
            if self.expected_income[-1] < np.mean(self.expected_income):
                self.spending = self.expected_income[-1]
            else:
                self.spending = np.mean(self.expected_income)
        else:
            if self.savings < 1.3 * self.expected_income[-1]:
                self.MPC = 0.8
            elif self.savings < 1.7 * self.expected_income[-1]:
                self.MPC = 0.95
            elif self.savings < 2 * self.expected_income[-1]:
                self.MPC = 1.04
            else:
                self.MPC = 1.3

            self.spending = np.mean(self.expected_income) * self.MPC

        return self.spending_basket

    def update_financial(self, interest_rate):
        """Household adjusts asset allocation.

        Args:
            interest_rate (float): Rate that the household receives on its
                savings.

        Returns:
            savings (float):

        """
        self.savings *= interest_rate
        return self.savings
