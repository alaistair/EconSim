""" Class for all information about a household """

class Household():

    def __init__(self):
        self.workers = 2 # labour endowment

        self.wages = [100]
        self.spending = [0]
        self.savings = [100]
        self.MPC = [0.9]

    def household_production(self, wages):
        self.wages.append(wages)
        print("Household wages = " + str(self.wages))
        return self.wages[-1]

    def household_consumption(self, wages):
        spending = wages * self.MPC[-1]
        self.spending.append(spending)
        print("Household spending = " + str(self.spending))

        savings = wages - spending
        self.savings.append(self.savings[-1] + savings)
        print("Household savings = " + str(self.savings))

        return self.spending[-1]

    def get_household_wages(self):
        return self.wages[-1]

    def get_household_savings(self):
        return self.savings[-1]

    def get_household_spending(self):
        return self.spending[-1]

    def get_household_status(self):
        print("Status")
        print(self.wages)
