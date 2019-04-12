""" Class for all information about an individual firm """
import random
import numpy as np
import math

class Firm():

    def __init__(self, settings):
        self.product_name = 'A'

        self.expected_production = settings.init_production
        self.production = 0 # flow of production (one cycle)
        self.product_price = 1 + (random.random() - 0.5) * 0.2
        self.inventory = int(0) # stock of inventory (units of output)
        self.revenue = 0 # flow of revenue (one cycle)
        self.profit = 0

        self.labour_productivity = settings.init_labour_productivity # output per labour input (1.05)
        self.labour_cost = 0
        self.capital_stock = settings.init_production
        self.capital_investment = 0
        self.debt = self.capital_stock
        self.capital_depreciation = settings.init_capital_depreciation # 0.04 (4%)

        self.workers = {} # hhID, worker dictionary
        self.owners = {} # hhID, owner dictionary

    def update_expected_production(self):
        # Update firm productivity based on capital spending
        #self.labour_productivity *= (1 + self.capital_investment/self.capital_stock)

        # Update firm's expected revenue based on past sales
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

    def update_hiring_intentions(self, interest_rate):
        expected_revenue = self.expected_production * self.product_price
        expected_labour_spending = expected_revenue/self.labour_productivity

        # Cobb-Douglas production function
        A = 1
        alpha = 0.3 # capital share of income
        log_expected_labour_spending = math.log(self.expected_production/(self.capital_stock**alpha))/(1-alpha)
        expected_labour_spending = math.exp(log_expected_labour_spending)

        expected_additional_labour_spending = expected_labour_spending
        print('ex additional labour spending ' + str(expected_additional_labour_spending))
        for hhID, household in self.workers.items():
            expected_additional_labour_spending -= np.mean(household.expected_income)

        return expected_additional_labour_spending

    def update_production(self, labour_cost):
        self.production += labour_cost * self.labour_productivity
        self.labour_cost += labour_cost
        self.debt += labour_cost
        return 1

    # Adds sales to firm's revenue.
    # Returns sales fulfilled
    def update_revenue(self, sales):
        quantity = sales/self.product_price
        if self.inventory > quantity: # firm fulfils all sales
            self.inventory -= quantity
            self.revenue += sales
        elif self.inventory > 0: # firm partially fulfils order
            sales = self.inventory * self.product_price
            self.revenue += sales
            self.inventory = 0
        elif self.inventory == 0: # firm out of stock, no sales
            sales = 0

        return sales

    def update_financial(self, interest_rate, CPI):
        cost_of_capital = self.capital_stock * (interest_rate - CPI + self.capital_depreciation)
        profit_rate = self.revenue - cost_of_capital
        self.profit = profit_rate - self.labour_cost
        self.labour_cost = 0

        if self.profit <= 0:
            self.capital_investment = 0
        else:
            self.capital_investment = self.profit * 0.5

        self.capital_stock = self.capital_stock * (1-self.capital_depreciation) + self.capital_investment
        self.debt = (self.debt + self.capital_investment - self.revenue) * interest_rate
        self.revenue = 0

        return self.profit

    def status(self):
        status = "Inventory: " + str(round(self.inventory,2)) + " production: " + str(round(self.production,2)) + " revenue: " + str(round(self.revenue,2)) + " debt: " + str(round(self.debt,2))
        return status
