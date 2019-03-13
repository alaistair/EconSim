""" Class for all information about a household """

class Household():

    def __init__(self, settings):
        self.people = 2 # labour endowment

        self.wages = 0 # income from working for one cycle
        self.spending = 0 # spending for one cycle
        self.savings = settings.init_hh_savings # stock of savings
        self.MPC = settings.init_MPC # 0.9
        self.human_capital = settings.init_human_capital # productive capacity, init = 100

    def household_production(self, wages):
        self.wages = wages
        return self.wages

    def household_consumption(self):
        if self.savings > 1.5 * self.wages:
            self.MPC = 1.15
            self.spending = self.wages * self.MPC
            self.wages *= (1 - self.MPC)
            self.savings += self.wages
            self.wages = 0
        else:
            self.MPC = 0.95
            self.spending = self.wages * self.MPC
            self.wages *= (1 - self.MPC)


        return self.spending

    def household_financial(self, interest_rate):
        self.savings *= interest_rate
        self.savings += self.wages
        self.wages = 0
        self.spending = 0

        return 0

    def status(self):
        status = "Income: " + str(round(self.wages,2)) + " savings: " + str(round(self.savings,2)) + " spending: " + str(round(self.spending,2))
        return status
