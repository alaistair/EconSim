""" Class for all information about a household """
import numpy as np
import random

class Household():

    def __init__(self, settings):
        self.people = 2 # labour endowment
        self.age = 18
        self.working = 'U'
        self.human_capital = np.random.normal(1, 0.25) # mean 1, sd 1
        if self.human_capital < 0: self.human_capital = 0 # no ZMP, for now

        self.expected_income = [10*self.human_capital, 10*self.human_capital, 10*self.human_capital] # pretax permanent income. Average of past three incomes
        self.income = 0 # income from working for one cycle
        self.savings = settings.init_household_savings # stock of savings (20)
        self.MPC = settings.init_MPC # 0.95

        self.spending = 0 # spending for one cycle
        self.spending_basket = [{'Name': 'A',
                            'Price': 1 + (random.random() - 0.5) * 0.1,
                            'Proportion': 1}] # proportion = % spending

    # Update expected income in light of current income. Expected wages rise with CPI,
    # but sticky wages mean expected wages flat if CPI < 0.
    def update_production(self, income):
        if income < 0: income = 0
        self.income = income
        return self.income

    # Decide how much to spend and how much to save
    def update_consumption(self):
        if self.savings <= self.expected_income[-1]:
            if self.expected_income[-1] < np.mean(self.expected_income): # no savings, income falling = paycheck to paycheck
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
        self.savings *= interest_rate
        return self.savings
