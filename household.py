""" Class for all information about a household """

class Household():

    def __init__(self):
        self.workers = 2 # labour endowment

        self.wages = 0
        self.consumption = 0
        self.savings = 0

    def household_production(self, wages):
        self.wages = wages
        print("Household wages = " + str(self.wages))
        self.savings += wages
        print("Household savings = " + str(self.savings))
        return self.wages

    def household_consumption(self, spending):
        self.consumption = spending
        print("Household spending = " + str(self.consumption))
        self.savings -= spending
        print("Household savings = " + str(self.savings))
        return self.consumption
