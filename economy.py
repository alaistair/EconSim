from household import Household
from firm import Firm
from random import randint

class Economy():

    # Initialise economy
    def __init__(self, initial_production):
        self.cycle = 0

        print("Initialise economy")
        self.households = []
        for i in range(0, 10):
            self.households.append(Household())

        self.firms = []
        for i in range(0, 10):
            self.firms.append(Firm())

        #self.firms[0].production[0] = 100
        #self.firms[0].inventory[0] = 100
        #self.households[0].wages[0] = 100
        #self.households[0].savings[0] = 100

    def production_market(self):
        print("Production cycle")
        self.households[0].household_production(
            self.firms[0].firm_production(
                self.firms[0].revenue[-1]))

    def consumption_market(self):
        print("Consumption cycle")

        total_spending = 0
        for household in self.households:
            total_spending += household.household_consumption(household.wages[-1])

        while total_spending > 0:
            i = randint(0, 9)
            print(str(i))
            self.firms[i].firm_revenue(10)
            total_spending -= 10

    def status(self):
        print("Status:")
        print("Firm production = " + str(self.firms[0].production))
        print("Firm revenue = " + str(self.firms[0].revenue))
        print("Firm inventory = " + str(self.firms[0].inventory))

        print("Household wages = " + str(self.households[0].wages))
        print("Household spending = " + str(self.households[0].spending))
        print("Household savings = " + str(self.households[0].savings))
        print("\n")

    def household_count(self):
        print("Household count")

    def household_add(self):
        print("Household add")

    def household_remove(self):
        print("Household remove")

    def firm_count(self):
        print("Firm count")

    def firm_add(self):
        print("Firm add")

    def firm_remove(self):
        print("Firm remove")

    def get_households_wages(self):
        households_wages = []
        for household in self.households:
            households_wages.append(household.get_household_wages())
        return households_wages

    def get_households_savings(self):
        households_savings = []
        for household in self.households:
            households_savings.append(household.get_household_savings())
        return households_savings

    def get_households_spending(self):
        households_spending = []
        for household in self.households:
            households_spending.append(household.get_household_spending())
        return households_spending
