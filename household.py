""" Class for all information about a household """

class Household():

    def __init__(self, hhID, settings):
        self.hhID = hhID
        self.people = 2 # labour endowment

        self.wages = 0 # income from working for one cycle
        self.spending = 0 # spending for one cycle
        self.savings = settings.init_savings # stock of savings
        self.MPC = settings.init_MPC

    def household_production(self, wages):
        self.wages = wages
        return self.wages

    def household_consumption(self):
        self.spending = self.wages * self.MPC
        self.wages *= (1 - self.MPC)
        return self.spending

    def household_financial(self, interest_rate):
        self.savings *= interest_rate
        self.savings += self.wages
        self.wages = 0
        self.spending = 0
