"""Kuznets Firm class."""

import random
import numpy as np


class Firm():
    """
    Kuznets Firm class.

    Each firm employs workers and capital to create a good. The quantity of
    output and the mix of inputs are determined by a Cobb-Douglas production
    function.

    Args:
        settings: Initial firm settings.

    Attributes:
        product_name: 'A' (only one product in economy for now)
        productivity:
        capital_investment:
        capital_stock:
        capital_share:
        human_capital:
        human_capital_share:
        labour_share:
        interest_rate:
        debt:
        capital_depreciation:
        expected_production:
        production:
        product_price:
        inventory:
        revenue:
        labour_cost:
        marginal_cost:
        max_price_gain:
        profit:
        workers:
        owners:

    """

    def __init__(self, settings):
        """Init Firm using Settings class."""
        self.product_name = 'A'
        self.productivity = settings.init_productivity
        self.capital_investment = 0
        self.capital_stock = 10 * random.choice([10, 20, 30])
        self.capital_share = 0.3
        self.human_capital = 0
        self.human_capital_share = 0.1
        self.labour_share = 1 - self.capital_share - self.human_capital_share

        self.interest_rate = settings.init_interest_rate + 0.02
        self.debt = self.capital_stock
        self.capital_depreciation = settings.init_capital_depreciation

        self.expected_production = self.capital_stock * .25
        self.production = 0
        self.product_price = 2 + (random.random() - 0.5) * 0.2
        self.inventory = int(0)
        self.revenue = 0
        self.labour_cost = 0
        self.marginal_cost = 0
        self.max_price_gain = 0.03  # stand in for product elasticity, for now
        self.profit = 0

        self.workers = {}  # {hhID, worker}
        self.owners = {}  # {hhID, owner}

    def update_expected_production(self, inflation):
        """
        Update firm's expected production.

        Each firm adjusts expected production ahead of hiring phase. Firm
        firstly reduces product price based on inventory, in an inverse method
        to price increases in economy consumption method. Then, the firm
        adjusts production to maximise profit at the point where marginal
        revenue = marginal cost.

        Args:
            inflation (float): Inflation is the GDP deflator.

        """
        self.product_price = self.product_price/(
            1 + self.inventory/self.expected_production * self.max_price_gain)

        total_labour_cost = 0
        for w in self.workers.values():
            total_labour_cost += np.mean(w.expected_income)
        marginal_production = (self.product_price + total_labour_cost)/(
            self.interest_rate - inflation + self.capital_depreciation
            + total_labour_cost)
        print('marginal_production ' + str(marginal_production))
        print('old ex p ' + str(self.expected_production))
        self.expected_production = (marginal_production
                                    * self.expected_production) - 1
        """
        print('ex p v2 ' + str(self.expected_production))
        self.expected_production = 1/(marginal_production - 1)
        print('ex p v3 ' + str(self.expected_production))


        marginal_production = self.product_price - (
            self.capital_stock + 1)*(
            self.interest_rate - inflation + self.capital_depreciation
            )/self.capital_stock
        marginal_production /= total_labour_cost
        self.expected_production = 1/(marginal_production - 1)
        print('ex p v3 ' + str(self.expected_production))
        """

    def get_marginal_cost(self, inflation):
        """
        Update firm's marginal cost.

        Marginal cost is the sum of the marginal cost of capital and the
        marginal cost of labour.

        Args:
            inflation (float): Inflation rate (1.05 === 5%)

        Returns:
            marginal_cost (float)

        """
        marginal_production = (self.production + 1)/self.production
        marginal_capital = (self.capital_stock + 1)/self.capital_stock
        marginal_cost_of_capital = marginal_capital * (
            self.interest_rate - inflation + self.capital_depreciation)

        """Marginal cost of labour. Assume labour costs constant."""
        total_labour_cost = 0
        for w in self.workers.values():
            total_labour_cost += np.mean(w.expected_income)
        marginal_cost_of_labour = (marginal_production
                                   - 1) * total_labour_cost

        self.marginal_cost = marginal_cost_of_capital + marginal_cost_of_labour
        self.marginal_cost = marginal_cost_of_capital
        print('self.interest_rate - inflation + self.capital_depreciation '
              + str(self.interest_rate - inflation
                    + self.capital_depreciation))
        print('self.interest_rate ' + str(self.interest_rate)
              + ' inflation ' + str(inflation)
              + ' cap d ' + str(self.capital_depreciation))

        return self.marginal_cost

    def marginal_revenue(self):
        """
        Calculate firm's marginal revenue.

        At this point we assume perfect competition, so all firms are price
        takers. Additional sales have no effect on supply/price, hence marginal
        revenue is the product price.
        """
        return self.product_price

    def update_hiring_intentions(self):
        """
        Calculate labour demand given capital stock and expected production.

        Solve for labour using Cobb-Douglas function:
        Y = A(K^alpha)(H^beta)(L^(1-alpha-beta))

        where A = self.productivity
              K = self.capital_stock
              alpha = self.capital_share
              H = self.human_capital
              beta = self.human_capital_share
              L = self.labour_cost
              gamma = self.labour_share

        Returns:
            int: 1 for hiring, -1 for firing, 0 for no change

        """
        # Calculate firm human capital
        labour_cost = 0
        for w in self.workers.values():
            labour_cost += np.mean(w.expected_income)
        human_capital = 0
        for w in self.workers.values():
            human_capital += (w.human_capital
                              * np.mean(w.expected_income)/labour_cost)

        if self.expected_production/(self.productivity
                                     * (self.capital_stock**self.capital_share)
                                     ) > ((human_capital
                                           ** self.human_capital_share)
                                          * (labour_cost**self.labour_share)):
            return 1
        else:
            return -1

        return 0

    def update_production(self):
        """Firm production function.

        Production is determined by a Cobb-Douglas function:
         Y = A(K^alpha)(H^beta)(L^(1-alpha-beta))

        where A = self.productivity
              K = self.capital_stock
              alpha = self.capital_share
              H = self.human_capital
              beta = self.human_capital_share
              L = self.labour_cost
              gamma = self.labour_share

        Returns:
            production (float):

        """
        # Calculate firm human capital
        for w in self.workers.values():
            self.labour_cost += np.mean(w.expected_income)
            w.update_production(np.mean(w.expected_income))
        self.human_capital = 0
        for w in self.workers.values():
            self.human_capital += w.human_capital * w.income/self.labour_cost

        self.production = (self.productivity
                           * (self.capital_stock**self.capital_share)
                           * (self.human_capital**self.human_capital_share)
                           * (self.labour_cost ** self.labour_share))

        return self.production

    def update_revenue(self, quantity, price):
        """
        Update firm's revenue based on sales, return the sales fulfilled.

        Args:
            quantity (float): Quantity of goods purchased.
            price (float): Price paid for given quantity of goods.

        Returns:
            sales (float): Sales fulfilled.

        """
        self.product_price = price
        sales = self.product_price * quantity
        if self.inventory > quantity:  # firm fulfils all sales
            self.inventory -= quantity
            self.revenue += sales
        elif self.inventory > 0:  # firm partially fulfils order
            sales = self.inventory * self.product_price
            self.revenue += sales
            self.inventory = 0
        elif self.inventory == 0:  # firm out of stock, no sales
            sales = 0

        return sales

    def update_financial(self, interest_rate, inflation):
        """
        Firm's financials.

        The firms takes its interest rate and inflation, calculates its profits
        and makes decisions relating to capital investment.

        Args:
            interest_rate (float): Interest rate firm pays for capital.
            inflation (float): Inflation rate (1.05 === 5%).

        Returns:
            profit (float): Firm's profit.

        """
        self.interest_rate = interest_rate

        cost_of_capital = self.capital_stock * (self.interest_rate - inflation
                                                + self.capital_depreciation)
        profit_rate = self.revenue - cost_of_capital
        labour_cost = 0
        for w in self.workers.values():
            labour_cost += np.mean(w.expected_income)
        self.profit = profit_rate - labour_cost  # - self.debt * interest_rate

        if self.profit <= 0:
            self.capital_investment = 0
        else:
            self.capital_investment = self.profit * 0.5

        self.capital_stock = self.capital_stock * (1 -
                                                   self.capital_depreciation
                                                   ) + self.capital_investment
        self.debt = (self.debt + self.capital_investment) * self.interest_rate

        return self.profit
