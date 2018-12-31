""" Class for all information about a household """

class Household():

    def __init__(self):
        self.workers = 2 # labour endowment

        self.wages = [0]
        self.consumption = [0]
        self.savings = [0]
        self.MPC = 0.9

    def household_production(self, wages):
        self.wages.append(wages)
        print("Household wages = " + str(self.wages))
        return self.wages[-1]

    def household_consumption(self, wages):
        self.household_savings(wages)
        consumption = wages * self.MPC
        self.consumption.append(consumption)
        print("Household spending = " + str(self.consumption))
        savings = wages - consumption
        self.savings.append(self.savings[-1] + savings)
        print("Household savings = " + str(self.savings))
        return self.consumption[-1]

    def household_savings(self, wages):
        if self.savings[-1] > wages:
            self.MPC = self.MPC * 1.05
        if self.savings[-1] < wages:
            self.MPC = self.MPC * 0.95
