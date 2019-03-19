""" Class for all information about an individual firm """
import random

class Firm():

    def __init__(self, settings):

        self.debt = settings.init_firm_debt # stock of debt
        self.revenue = 0 # flow of revenue (one cycle)

        self.product_name = 'A'
        self.inventory = int(0) # stock of inventory (units of output)
        self.expected_production = settings.init_production
        self.production = 0 # flow of production (one cycle)

        self.product_price = 1 + (random.random() - 0.5) * 0.2

        self.productivity = settings.init_productivity # output per labour input

        self.workers = {} # hhID, worker dictionary
        self.owners = {} # hhID, owner dictionary
        self.init = 1

    def firm_production(self):
        # Update firm's expected revenue based on sales
        if self.init:
            self.init = 0
        else:
            if self.inventory == 0: # Ran out of inventory
                self.product_price *= 1.1
                self.expected_production *= 1.1
            elif self.inventory > 0.5 * self.expected_production:
                self.product_price *= 0.97
                self.expected_production *= 0.97
            else:
                self.product_price *= 1.01
                self.expected_production *= 1.01

        if self.product_price < 0: self.product_price = 0.01

        self.production = self.expected_production

        labour_cost = self.production/self.productivity # $
        self.debt += labour_cost
        return labour_cost

    # Adds sales to firm's revenue.
    # Returns sales fulfilled
    def firm_revenue(self, sales):
        quantity = sales/self.product_price
        if self.inventory > quantity: # firm fulfils all sales
            self.inventory -= quantity
            self.revenue += sales
            return sales
        elif self.inventory > 0: # firm partially fulfils order, returns unfilled amount
            sales = self.inventory * self.product_price
            self.revenue += sales
            self.inventory = 0
            return sales
        elif self.inventory == 0: # firm out of stock, return sales
            return 0

    def firm_financial(self, interest_rate):
        self.debt *= interest_rate
        self.debt -= self.revenue
        self.revenue = 0

        return 0

    def status(self):
        status = "Inventory: " + str(round(self.inventory,2)) + " production: " + str(round(self.production,2)) + " revenue: " + str(round(self.revenue,2)) + " debt: " + str(round(self.debt,2))
        return status
