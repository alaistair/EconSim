""" Class for all information about an individual firm """

class Firm():

    def __init__(self):
        self.production = [100]
        self.revenue = [100]
        self.inventory = [0]

    def firm_production(self, revenue):
        if self.inventory[-1] < 0:
            production = revenue - self.inventory[-1]
        elif self.inventory[-1] > 0.5 * revenue:
            production = 0.5 * revenue
            self.inventory[-1] -= 0.5 * revenue
        elif self.inventory[-1] > 0.1 * revenue:
            production = 0.9 * revenue
            self.inventory[-1] -= 0.1 * revenue
        else:
            production = revenue

        self.production.append(production)

        print("Firm production = " + str(self.production))
        return production

    def firm_revenue(self, sales):
        self.revenue.append(sales)
        print("Firm sales = " + str(self.revenue))
        self.inventory.append(self.inventory[-1] + self.production[-1] - self.revenue[-1])
        print("Firm inventory = " + str(self.inventory))
        return self.revenue[-1]

    def get_firm_production(self):
        return self.production[-1]

    def get_firm_inventory(self):
        return self.inventory[-1]

    def get_firm_revenue(self):
        return self.revenue[-1]
