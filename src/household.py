""" Class for all information about a household """
import random

class Household():

    def __init__(self, settings):
        self.people = 2 # labour endowment
        self.age = 18
        self.human_capital = random.choice(settings.init_human_capital) #[10,20,30]

        self.expected_wages = self.human_capital
        self.wages = 0 # income from working for one cycle
        self.savings = settings.init_household_savings # stock of savings
        self.MPC = settings.init_MPC # 0.95

        self.spending = 0 # spending for one cycle
        self.spending_basket = [{'Name': 'A',
                            'Price': 1 + (random.random() - 0.5) * 0.1,
                            'Proportion': 1}] # proportion = % spending

    def update_production(self, wages, CPI):
        self.wages = wages
        if CPI > 1:
            self.expected_wages = wages * CPI
        else:
            self.expected_wages = wages

    # Decide how much to spend and how much to save
    def update_consumption(self):
        if self.savings < 0.3 * self.wages:
            self.MPC = 0.8
            self.spending = self.wages * self.MPC
            self.wages *= (1 - self.MPC)
        elif self.savings < 0.7 * self.wages:
            self.MPC = 0.95
            self.spending = self.wages * self.MPC
            self.wages *= (1 - self.MPC)
        elif self.savings < 1 * self.wages:
            self.MPC = 1.04
            self.spending = self.wages * self.MPC
            self.wages *= (1 - self.MPC)
            self.savings += self.wages
            self.wages = 0
        else:
            self.MPC = 1.3
            self.spending = self.wages * self.MPC
            self.wages *= (1 - self.MPC)
            self.savings += self.wages
            self.wages = 0

        return self.spending_basket

    def update_financial(self, interest_rate):
        self.savings *= interest_rate
        self.savings += self.wages
        self.wages = 0
        self.spending = 0

        return 0

    def status(self):
        status = "Income: " + str(round(self.wages,2)) + " savings: " + str(round(self.savings,2)) + " spending: " + str(round(self.spending,2))
        return status
