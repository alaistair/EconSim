""" Class for all information about an individual firm """

class Firm():

    def __init__(self):

        self.production = 0
        self.revenue = 0
        self.inventory = 0

    def firm_production(self, production):
        self.production = production
        print("Firm production = " + str(self.production))
        self.inventory += production
        print("Firm inventory = " + str(self.inventory))
        return self.production

    def firm_revenue(self, sales):
        self.revenue = sales
        print("Firm sales = " + str(self.revenue))
        self.inventory -= sales
        print("Firm inventory = " + str(self.inventory))
        return self.revenue
