""" Class for all information about a household """
import numpy as np
import random

class Household():

    def __init__(self, settings):
        self.people = 2 # labour endowment
        self.age = 18
        self.human_capital = random.choice(settings.init_human_capital) #[10,20,30]

        self.expected_income = [self.human_capital, self.human_capital, self.human_capital] # permanent income. Average of past three incomes
        self.income = 0 # income from working for one cycle
        self.savings = settings.init_household_savings # stock of savings
        self.MPC = settings.init_MPC # 0.95

        self.spending = 0 # spending for one cycle
        self.spending_basket = [{'Name': 'A',
                            'Price': 1 + (random.random() - 0.5) * 0.1,
                            'Proportion': 1}] # proportion = % spending

    # Update expected income in light of current income. Expected wages rise with CPI,
    # but sticky wages mean expected wages flat if CPI < 0.
    def update_production(self, income, CPI):
        self.expected_income.pop()
        if income < 0: income = 0
        self.income = income
        if CPI > 1:
            self.expected_income.append(income * CPI)
        else:
            self.expected_income.append(income)
        return self.expected_income

    # Decide how much to spend and how much to save
    def update_consumption(self):
        if self.savings <= 0:
            if self.income < np.mean(self.expected_income): # paycheck to paycheck
                self.spending = self.income
            else:
                self.spending = np.mean(self.expected_income)
                self.savings = self.income - np.mean(self.expected_income)
        else:
            if self.savings < 0.3 * self.income:
                self.MPC = 0.8
            elif self.savings < 0.7 * self.income:
                self.MPC = 0.95
            elif self.savings < 1 * self.income:
                self.MPC = 1.04
            else:
                self.MPC = 1.3

            self.spending = np.mean(self.expected_income) * self.MPC
            self.savings = self.savings + self.income - self.spending
        self.income = 0

        return self.spending_basket

    def update_financial(self, interest_rate):
        self.savings *= interest_rate
        self.savings += self.income
        self.income = 0
        self.spending = 0

        return 0

    def status(self):
        status = "Income: " + str(round(self.income,2)) + " savings: " + str(round(self.savings,2)) + " spending: " + str(round(self.spending,2))
        return status
