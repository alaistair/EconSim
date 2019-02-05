""" Class for all information about a household """

class Household():

    def __init__(self, hhID):
        self.hhID = hhID
        self.people = 2 # labour endowment

        self.wages = 100 # income from working for one cycle
        self.spending = 0 # spending for one cycle
        self.savings = 100 # stock of savings
        self.MPC = 0.9

    def household_production(self, wages):
        self.wages = wages
        return self.wages

    def household_consumption(self, wages):
        self.spending = wages * self.MPC
        self.savings += wages * (1 - self.MPC)
        return self.spending

    def get_household_data(self):
        data = {'hhID': self.hhID,
                'income': [self.wages],
                'savings': [self.savings],
                'spending': [self.spending]}
        return data

    def get_household_ID(self):
        return self.hhID
