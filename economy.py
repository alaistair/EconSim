from household import Household
from firm import Firm
from random import randint

class Economy():

    # Initialise economy
    def __init__(self, initial_production):
        self.cycle = 0
        self.households = []
        self.households.append(Household())
        self.firms = []
        self.firms.append(Firm())

        print("Initial production")
        self.households[self.cycle].household_production(
            self.firms[self.cycle].firm_production(initial_production))

    def production(self):
        print("Production")
        self.households[self.cycle].household_production(
            self.firms[self.cycle].firm_production(
                self.firms[self.cycle].revenue))

    def consumption(self):
        print("Consumption")
        self.firms[self.cycle].firm_revenue(
            self.households[self.cycle].household_consumption(
                self.households[self.cycle].savings))
        #self.cycle += 1


    def status(self):
        """print("Status: cycle " + str(self.cycle))
        print("Firm production = " + str(self.firms[0].production))
        print("Firm revenue = " + str(self.firms[0].revenue))
        print("Firm inventory = " + str(self.firms[0].inventory))

        print("Household wages = " + str(self.households[0].wages))
        print("Household consumption = " + str(self.households[0].consumption))
        print("Household savings = " + str(self.households[0].savings))"""
        print("\n")
