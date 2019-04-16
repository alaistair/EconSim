""" Class for all information about an individual firm """
import random
import numpy as np
import math

class Firm():

    def __init__(self, settings):
        self.product_name = 'A'

        self.expected_production = float(settings.init_production)
        self.production = 0 # flow of production (one cycle)
        self.product_price = 2 + (random.random() - 0.5) * 0.2
        self.inventory = int(0) # stock of inventory (units of output)
        self.revenue = 0 # flow of revenue (one cycle)
        self.labour_cost = 0
        self.profit = 0

        self.productivity = settings.init_productivity # output per capital/labour input (1.05)
        self.capital_investment = 0
        self.capital_stock = settings.init_production
        self.capital_share = 0.3 # 'alpha' in Cobb-Douglas production function
        self.human_capital = 0
        self.human_capital_share = 0.1 # 'beta'
        self.labour_share = 1 - self.capital_share - self.human_capital_share # 'gamma'

        self.debt = self.capital_stock
        self.capital_depreciation = settings.init_capital_depreciation # 0.04 (4%)

        self.workers = {} # hhID, worker dictionary
        self.owners = {} # hhID, owner dictionary

    def update_expected_production(self):
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

    def update_hiring_intentions(self):
        # Cobb-Douglas production function
        # Y = A(K^alpha)(H^beta)(L^(1-alpha-beta))
        A = self.productivity
        alpha = self.capital_share # capital share of income
        beta = self.human_capital_share
        gamma = self.labour_share

        expected_labour_spending = self.expected_production/(A * (self.capital_stock**alpha))

        # calculate firm human capital
        self.labour_cost = 0
        self.human_capital = 0
        for hhID, w in self.workers.items():
            self.labour_cost += w.update_production(np.mean(w.expected_income))

        for w in self.workers.values():
            self.human_capital += w.human_capital * w.income/self.labour_cost

        if self.expected_production/(A * (self.capital_stock**alpha)) > (self.human_capital**beta) * (self.labour_cost**gamma):
            return 1 # hiring
        else:
            return -1 # firing

        return 0 # labour force optimal

    def update_production(self):
        # Cobb-Douglas production function
        A = self.productivity
        alpha = self.capital_share # capital share of income
        beta = self.human_capital_share
        gamma = self.labour_share

        self.production = A * (self.capital_stock ** alpha) * (self.human_capital ** beta) * (self.labour_cost ** gamma)
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
