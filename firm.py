""" Class for all information about an individual firm """

class Firm():

    def __init__(self, settings):

        self.expected_revenue = settings.init_firm_expected_revenue # = 100
        self.capital = 0
        self.debt = settings.init_firm_debt # stock of debt
        self.inventory = 0 # stock of inventory
        self.production = 0 # flow of production (one cycle)
        self.productivity = settings.init_productivity # output per labour input
        self.revenue = 0 # flow of revenue (one cycle)
        self.workers = {} # hhID, worker dictionary
        self.owners = {} # hhID, owner dictionary

    def firm_production(self):
        # Update firm's expected revenue based on sales
        if self.inventory == 0: # Ran out of inventory
            self.expected_revenue *= 1.1
        else:
            self.expected_revenue -= self.inventory/4
        if self.expected_revenue < 0: self.expected_revenue = 0

        self.production = self.expected_revenue
        labour_cost = self.production/self.productivity
        self.debt += labour_cost
        return labour_cost

    # Adds sales to firm's revenue.
    # Return 0 if sales fulfilled, return residual if inventory run out
    def firm_revenue(self, sales):
        if self.inventory > sales: # firm fulfils all sales
            self.inventory -= sales
            self.revenue += sales
            return 0
        elif self.inventory > 0: # firm partially fulfils order, returns unfilled amount
            self.revenue += self.inventory
            sales -= self.inventory
            self.inventory = 0
            return sales
        elif self.inventory == 0: # firm out of stock, return sales
            return sales

    def firm_financial(self, interest_rate):
        self.debt *= interest_rate
        self.debt -= self.revenue
        self.revenue = 0

        return 0
