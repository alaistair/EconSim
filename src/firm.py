""" Class for all information about an individual firm """
import random
import numpy as np
import math

class Firm():

    def __init__(self, settings):
        self.product_name = 'A'
        self.productivity = settings.init_productivity # output per capital/labour input (1.05)
        self.capital_investment = 0
        self.capital_stock = 10* random.choice([10,20,30])#settings.init_production
        self.capital_share = 0.3 # 'alpha' in Cobb-Douglas production function
        self.human_capital = 0
        self.human_capital_share = 0.1 # 'beta'
        self.labour_share = 1 - self.capital_share - self.human_capital_share # 'gamma'

        self.interest_rate = settings.init_interest_rate + 0.02
        self.debt = self.capital_stock
        self.capital_depreciation = settings.init_capital_depreciation # 0.03 (3%)

        self.expected_production = self.capital_stock * .25
        self.production = 0 # flow of production (one cycle)
        self.product_price = 2 + (random.random() - 0.5) * 0.2
        self.inventory = int(0) # stock of inventory (units of output)
        self.revenue = 0 # flow of revenue (one cycle)
        self.labour_cost = 0
        self.marginal_cost = 0
        self.max_price_gain = 0.03 # stand in for product elasticity, for now
        self.profit = 0

        self.workers = {} # hhID, worker dictionary
        self.owners = {} # hhID, owner dictionary

    def update_expected_production(self, inflation):
        # Firm walks price down based on inventory. Inverse method to price increases in economy consumption method.
        self.product_price = self.product_price / (1 + self.inventory/self.expected_production * self.max_price_gain)

        # Firm updates production to max profit (where marginal revenue = marginal cost
        total_labour_cost = 0
        for w in self.workers.values():
            total_labour_cost += np.mean(w.expected_income)
        marginal_production = (self.product_price + total_labour_cost)/(self.interest_rate - inflation + self.capital_depreciation + total_labour_cost)
        print('marginal_production ' + str(marginal_production))
        print('old ex p ' + str(self.expected_production))
        self.expected_production = marginal_production * self.expected_production - 1
        #print('ex p v2 ' + str(self.expected_production))
        #self.expected_production = 1/(marginal_production - 1)
        #print('ex p v3 ' + str(self.expected_production))


        #marginal_production = self.product_price - (self.capital_stock + 1)*(self.interest_rate - inflation + self.capital_depreciation)/self.capital_stock
        #marginal_production /= total_labour_cost
        #self.expected_production = 1/(marginal_production - 1)
        #print('ex p v3 ' + str(self.expected_production))




    def get_marginal_cost(self, inflation):
        marginal_production = (self.production + 1)/self.production
        marginal_capital = (self.capital_stock + 1)/self.capital_stock
        marginal_cost_of_capital = marginal_capital * (self.interest_rate - inflation + self.capital_depreciation)

        total_labour_cost = 0
        for w in self.workers.values():
            total_labour_cost += np.mean(w.expected_income)
        marginal_cost_of_labour = (marginal_production - 1) * total_labour_cost # assume labour costs constant

        #self.marginal_cost = marginal_cost_of_capital + marginal_cost_of_labour
        self.marginal_cost =  marginal_cost_of_capital
        print('self.interest_rate - inflation + self.capital_depreciation ' + str(self.interest_rate - inflation + self.capital_depreciation))
        print('self.interest_rate ' + str(self.interest_rate) + ' inflation ' + str(inflation) + ' cap d ' + str(self.capital_depreciation))

        return self.marginal_cost

    def marginal_revenue(self):
        # Assuming perfect competition, ie firm is price taker
        return self.product_price

    def update_hiring_intentions(self):
        # Cobb-Douglas production function
        # Y = A(K^alpha)(H^beta)(L^(1-alpha-beta))
        A = self.productivity
        alpha = self.capital_share # capital share of income
        beta = self.human_capital_share
        gamma = self.labour_share

        # calculate firm human capital
        labour_cost = 0
        for w in self.workers.values():
            labour_cost += np.mean(w.expected_income)

        human_capital = 0
        for w in self.workers.values():
            human_capital += w.human_capital * np.mean(w.expected_income)/labour_cost

        if self.expected_production/(A * (self.capital_stock**alpha)) > (human_capital**beta) * (labour_cost**gamma):
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

        # calculate firm human capital
        for w in self.workers.values():
            self.labour_cost += np.mean(w.expected_income)
            w.update_production(np.mean(w.expected_income))
        self.human_capital = 0
        for w in self.workers.values():
            self.human_capital += w.human_capital * w.income/self.labour_cost

        self.production = A * (self.capital_stock ** alpha) * (self.human_capital ** beta) * (self.labour_cost ** gamma)

        return 1

    # Adds sales to firm's revenue.
    # Returns sales fulfilled
    def update_revenue(self, quantity, price):
        self.product_price = price
        sales = self.product_price * quantity
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

    def update_financial(self, interest_rate, inflation):
        self.interest_rate = interest_rate

        cost_of_capital = self.capital_stock * (self.interest_rate - inflation + self.capital_depreciation)
        profit_rate = self.revenue - cost_of_capital
        labour_cost = 0
        for w in self.workers.values():
            labour_cost += np.mean(w.expected_income)
        self.profit = profit_rate - labour_cost #- self.debt * interest_rate

        if self.profit <= 0:
            self.capital_investment = 0
        else:
            self.capital_investment = self.profit * 0.5

        self.capital_stock = self.capital_stock * (1-self.capital_depreciation) + self.capital_investment
        self.debt = (self.debt + self.capital_investment) * self.interest_rate

        return self.profit
