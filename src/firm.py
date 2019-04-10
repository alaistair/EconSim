""" Class for all information about an individual firm """
import random
import numpy as np

class Firm():

    def __init__(self, settings):
        self.product_name = 'A'

        self.expected_production = settings.init_production
        self.production = 0 # flow of production (one cycle)
        self.product_price = 1 + (random.random() - 0.5) * 0.2
        self.inventory = int(0) # stock of inventory (units of output)
        self.revenue = 0 # flow of revenue (one cycle)
        self.profit = 0

        self.labour_productivity = settings.init_labour_productivity # output per labour input
        self.capital_stock = settings.init_production
        self.capital_investment = 0
        self.debt = self.capital_stock
        self.capital_depreciation = settings.init_capital_depreciation # 0.04 (4%)

        self.workers = {} # hhID, worker dictionary
        self.owners = {} # hhID, owner dictionary

    def update_hiring_intentions(self, interest_rate):
        # Update firm productivity based on capital spending
        #self.labour_productivity *= (1 + self.capital_investment/self.capital_stock)
        self.capital_investment = 0 # this should probably be moved somewhere else at some point

        # Update firm's expected revenue based on sales
        if self.inventory == 0: # Ran out of inventory
            self.product_price *= 1.1
            self.expected_production *= 1.1
        elif self.inventory > 0.5 * self.expected_production: # too much inventory
            self.product_price *= 0.9
            self.expected_production *= 0.95
        else:
            self.product_price *= 1.02
            self.expected_production *= 1.02
        if self.product_price < 0: self.product_price = 0.01

        expected_revenue = self.expected_production * self.product_price
        expected_production_spending = expected_revenue - self.debt * (interest_rate + 0.5 - 1) - self.capital_investment
        expected_labour_spending = expected_production_spending/self.labour_productivity
        expected_additional_labour_spending = expected_labour_spending
        for hhID, household in self.workers.items():
            expected_additional_labour_spending -= np.mean(household.expected_income)

        if expected_additional_labour_spending < 0:
            return 0
        else:
            return expected_additional_labour_spending

    def update_production(self, labour_cost):
        self.production += labour_cost * self.labour_productivity
        self.debt += labour_cost
        return 1

    # Adds sales to firm's revenue.
    # Returns sales fulfilled
    def update_revenue(self, sales):
        quantity = sales/self.product_price
        if self.inventory > quantity: # firm fulfils all sales
            self.inventory -= quantity
            self.revenue += sales
            return sales
        elif self.inventory > 0: # firm partially fulfils order
            sales = self.inventory * self.product_price
            self.revenue += sales
            self.inventory = 0
            return sales
        elif self.inventory == 0: # firm out of stock, no sales
            return 0

    def update_financial(self, interest_rate, CPI):
        cost_of_capital = self.capital_stock * (interest_rate - CPI + self.capital_depreciation)
        profit_rate = self.revenue - cost_of_capital
        self.profit = profit_rate
        if profit_rate <= 0:
            self.capital_investment = 0
        else:
            self.capital_investment = (self.revenue - cost_of_capital) * 0.5

        self.capital_stock = self.capital_stock * (1-self.capital_depreciation) + self.capital_investment
        self.debt = (self.debt + self.capital_investment - self.revenue) * interest_rate
        self.revenue = 0

        return profit_rate

    def status(self):
        status = "Inventory: " + str(round(self.inventory,2)) + " production: " + str(round(self.production,2)) + " revenue: " + str(round(self.revenue,2)) + " debt: " + str(round(self.debt,2))
        return status
