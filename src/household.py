""" Class for all information about a household """
import random

class Household():

    def __init__(self, settings):
        self.people = 2 # labour endowment
        self.age = 18
        self.human_capital = random.choice(settings.init_human_capital) #[10,20,30]

        self.expected_income = [self.human_capital, self.human_capital, self.human_capital]# permanent income
        self.income = 0 # income from working for one cycle
        self.savings = settings.init_household_savings # stock of savings
        self.MPC = settings.init_MPC # 0.95

        self.spending = 0 # spending for one cycle
        self.spending_basket = [{'Name': 'A',
                            'Price': 1 + (random.random() - 0.5) * 0.1,
                            'Proportion': 1}] # proportion = % spending

    def update_production(self, income, CPI):
        self.income = income
        self.expected_income.pop()
        if CPI > 1:
            self.expected_income.append(income * CPI)
        else:
            self.expected_income.append(income)

    # Decide how much to spend and how much to save
    def update_consumption(self):
        if self.savings < 0.3 * self.income:
            self.MPC = 0.8
            self.spending = self.income * self.MPC
            self.income *= (1 - self.MPC)
        elif self.savings < 0.7 * self.income:
            self.MPC = 0.95
            self.spending = self.income * self.MPC
            self.income *= (1 - self.MPC)
        elif self.savings < 1 * self.income:
            self.MPC = 1.04
            self.spending = self.income * self.MPC
            self.income *= (1 - self.MPC)
            self.savings += self.income
            self.income = 0
        else:
            self.MPC = 1.3
            self.spending = self.income * self.MPC
            self.income *= (1 - self.MPC)
            self.savings += self.income
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
