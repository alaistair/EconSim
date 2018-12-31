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

        print("Initialise economy")
        self.firms[0].production[0] = 100
        self.firms[0].inventory[0] = 100
        self.households[0].wages[0] = 100
        self.households[0].savings[0] = 100

    def production(self):
        print("Production cycle")
        self.households[0].household_production(
            self.firms[0].firm_production(
                self.firms[0].revenue[-1]))

    def consumption(self):
        print("Consumption cycle")
        self.firms[0].firm_revenue(
            self.households[0].household_consumption(
                self.households[0].wages[-1]))
        #self.cycle += 1


    def status(self):
        print("Status:")
        print("Firm production = " + str(self.firms[0].production))
        print("Firm revenue = " + str(self.firms[0].revenue))
        print("Firm inventory = " + str(self.firms[0].inventory))

        print("Household wages = " + str(self.households[0].wages))
        print("Household spending = " + str(self.households[0].consumption))
        print("Household savings = " + str(self.households[0].savings))
        print("\n")
