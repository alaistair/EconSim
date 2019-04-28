"""Kuznets Economy class."""

from __future__ import division
from collections import defaultdict
from Kuznets.household import Household
from Kuznets.firm import Firm
from Kuznets.government import Government
import random
import numpy as np
import pandas as pd
#  from functools import reduce

#  import Kuznets.updateeconomydata as updateeconomydata
#  import time


class Economy():
    """
    Kuznets Economy class.

    Each economy contains households and firms that interact for the purposes
    of production and consumption. Intertemporal activity is incorporated via
    financial markets, and the government works to redistribute funds to
    support the unemployed.

    Args:
        settings (Kuznets.settings): Initial economy settings.

    Attributes:
        time (int): +1 every cycle.

        households (dict): {hhID, household}.
        firms (dict): {firmID, firm}.
        government (object):

        households_data (dataframe): Key data for each household (human
            capital, expected income, income, life_stage, spending, savings).
            MultiIndex is hhID, time, cycle (production, consumption,
            financial).
        firms_data (dataframe): Key data for each firm (expected prodcution,
            production, product price, revenue, inventory, labour cost,
            workers, capital investment', capital stock, marginal cost, debt,
            profit). MultiIndex is firmID, time, cycle (p, c, f).
        government_data (dataframe): Key government data (revenue, expenditure,
            debt). MultiIndex is time, cycle (p, c, f).
        economy_data (dataframe): Key aggregate economic data ('household
            income, household savings, household spending, household expected
            income, firm inventory, firm production, firm revenue, firm debt,
            firm profit, CPI, interest rate, unemployment rate). MultiIndex is
            time, cycle (p, c, f).

        GDP (float): Calculated on production basis (total firm revenue
            + inventories valued at market price).
        CPI (float): Inflation.
        interest_rate (float): Equivalent to monetary policy rate.
        unemployment_rate (float):
        products (defaultdict): List of all products made in economy.

    """

    def __init__(self, settings):
        """Init Economy with Settings."""
        self.time = int(0)

        self.households = {i: Household(settings) for i in
                           range(settings.init_households)}
        self.firms = {i: Firm(settings) for i in range(settings.init_firms)}
        self.government = Government(settings)

        tuples = [(self.time, 'p', i) for i in range(settings.init_households)]
        self.households_data = pd.DataFrame({
            'Human capital': [0.],
            'Expected income': [0.],
            'Income': [0.],
            'Life stage': [""],
            'Spending': [0.],
            'Savings': [0.],
            }, index=pd.MultiIndex.from_tuples(tuples, names=[
                'time', 'cycle', 'hhID']))

        tuples = [(self.time, 'p', i) for i in range(settings.init_firms)]
        self.firms_data = pd.DataFrame({
            'Expected production': [0.],
            'Production': [0.],
            'Product price': [0.],
            'Revenue': [0.],
            'Inventory': [0.],
            'Labour cost': [0.],
            'Workers': [0],
            'Capital investment': [0.],
            'Capital stock': [0.],
            'Marginal cost': [0.],
            'Debt': [0.],
            'Profit': [0.],
            }, index=pd.MultiIndex.from_tuples(tuples, names=[
                'time', 'cycle', 'firmID']))

        tuples = [(self.time, 'p')]
        self.government_data = pd.DataFrame({
            'Revenue': [0.],
            'Expenditure': [0.],
            'Debt': [0.],
            }, index=pd.MultiIndex.from_tuples(tuples, names=[
                'time', 'cycle']))

        self.economy_data = pd.DataFrame({
            'Household income': [0.],
            'Household savings': [0.],
            'Household spending': [0.],
            'Household expected income': [0.],
            'Firm inventory': [0.],
            'Firm production': [0.],
            'Firm revenue': [0.],
            'Firm debt': [0.],
            'Firm profit': [0.],
            'CPI': [0.],
            'Interest rate': [0.],
            'Unemployment rate': [0.],
            }, index=pd.MultiIndex.from_tuples(tuples, names=[
                'time', 'cycle']))

        self.GDP = 0
        self.CPI = 2
        self.interest_rate = settings.init_interest_rate
        self.unemployment_rate = settings.init_unemployment_rate

        self.products = defaultdict(list)

        # Allocate firms to product
        for firmID, firm in self.firms.items():
            self.products[firm.product_name].append(firmID)

        # Initialise labour market
        # Every firm gets at least one worker
        workers = (1 - self.unemployment_rate) * len(self.households.keys())
        workers_per_firm = int(workers/len(self.firms.keys()))

        for i in range(workers_per_firm):
            for firmID, firm in self.firms.items():
                hhID, household = random.choice(list(
                                    self.get_unemployed().items()))
                firm.workers[hhID] = household
                household.life_stage = 'E'

        # Firms update expected production given labour force and capital stock
        '''for f in self.firms.values():
            A = f.productivity
            alpha = f.capital_share # capital share of income
            beta = f.human_capital_share
            gamma = f.labour_share

            labour_cost = 0
            for w in f.workers.values():
                labour_cost += np.mean(w.expected_income)
            human_capital = 0
            for w in f.workers.values():
                human_capital += w.human_capital * w.income/labour_cost

            f.expected_production = A * (f.capital_stock ** alpha) *
                            (human_capital ** beta) * (labour_cost ** gamma)'''

        self.worker_hiring()

        for f in self.firms.values():
            f.update_production()
            f.get_marginal_cost(self.growth_rate(self.economy_data['CPI']))

        self.government.income_tax(self.households)
        self.government.welfare(self.get_income_per_capita(),
                                self.get_unemployed())
        for h in self.households.values():
            h.update_income_expectations(1, self.government.income_tax_rate)
        self.accounting_pre()

        # update economy dataframe
        for i in range(2):  # fix weird bug
            for hhID, household in self.households.items():
                self.households_data.loc[(self.time, 'p', hhID)] = {
                    'Human capital': household.human_capital,
                    'Expected income': np.mean(household.expected_income),
                    'Income': household.income,
                    'Life stage': household.life_stage,
                    'Spending': household.spending,
                    'Savings': household.savings, }

        for i in range(2):  # fix weird bug
            for firmID, firm in self.firms.items():
                self.firms_data.loc[(self.time, 'p', firmID)] = {
                    'Expected production': float(firm.expected_production),
                    'Production': firm.production,
                    'Product price': firm.product_price,
                    'Revenue': firm.revenue,
                    'Inventory': firm.inventory,
                    'Labour cost': firm.labour_cost,
                    'Workers': len(firm.workers.keys()),
                    'Capital investment': firm.capital_investment,
                    'Capital stock': firm.capital_stock,
                    'Marginal cost': firm.marginal_cost,
                    'Debt': firm.debt,
                    'Profit': firm.profit, }

        self.government_data = pd.DataFrame({
            'Revenue': self.government.revenue,
            'Expenditure': self.government.expenditure,
            'Debt': self.government.debt,
            }, index=pd.MultiIndex.from_tuples(tuples, names=[
                'time', 'cycle']))

        df1 = self.households_data.xs('p', level='cycle').groupby(
            level=0).sum().loc[self.time]
        df2 = self.firms_data.xs('p', level='cycle').groupby(
            level=0).sum().loc[self.time]

        self.economy_data.loc[(self.time, 'p')] = {
            'Household income': float(df1['Income']),
            'Household savings': float(df1['Savings']),
            'Household spending': float(df1['Spending']),
            'Household expected income':
                float(np.mean(df1['Expected income'])),
            'Firm inventory': float(df2['Inventory']),
            'Firm production': float(df2['Production']),
            'Firm revenue': float(df2['Revenue']),
            'Firm debt': float(df2['Debt']),
            'Firm profit': float(df2['Profit']),
            'CPI': float(self.CPI),
            'Interest rate': float(self.interest_rate),
            'Unemployment rate':
                float(len(self.get_unemployed().keys())/len(self.households)),
            }

        self.accounting_post()
        self.move_production_to_inventory()
        self.consumption_market()
        self.calculate_CPI()
        self.update_economy_data('c')
        self.financial_market()
        self.update_economy_data('f')

    def worker_seperations(self):
        """
        Worker seperations.

        First step in labour market. If firm has more two or more workers, one
        will quit to create labour force churn. Firms will then randomly fire
        workers to reduce labour in line with their expected production,
        leaving at least one worker.
        """
        for f in self.firms.values():
            if len(f.workers) > 1:  # One worker quits
                hhID, household = random.choice(list(f.workers.items()))
                household.life_stage = 'U'
                del f.workers[hhID]

            # Firm reduces labour further if necessary
            while f.update_hiring_intentions() == -1:
                if len(f.workers) > 1:
                    hhID, household = random.choice(list(
                        f.workers.items()))
                    household.life_stage = 'U'
                    del f.workers[hhID]
                else:
                    print('only one worker left in firm')
                    break

    def worker_hiring(self):
        """
        Worker hiring.

        Second step in labour market. Each firm hires labour to meet their
        expected production goals.
        """
        hiring = True
        while hiring:
            hiring = False

            hiring_firms = [firm for firm in self.firms.values()
                            if firm.update_hiring_intentions() == 1]

            if not hiring_firms:
                break

            random.shuffle(hiring_firms)
            for firm in hiring_firms:
                # check if economy already at lowest rate of unemployment
                if len(self.get_unemployed().keys()) <= 1:
                    hiring = False
                    break

                # Firm uses '37% rule' to hire, ie picks best candidate from
                # random 37% subset of candidates
                candidates = int(0.37 * len(self.get_unemployed().keys()))
                # Ensure at least one candidate in consideration
                if candidates < 1:
                    candidates = 1
                candidate_list = {}
                # Choose candidates randomly from unemployed
                for i in range(0, candidates):
                    candidate = random.choice(
                                list(self.get_unemployed().keys()))
                    candidate_list[candidate] = self.get_unemployed()[
                        candidate]

                # Find best candidate.
                # Change this in future to allow diff hc needs
                best_candidate_hhID = -1
                best_candidate_human_capital = -1
                for hhID, household in candidate_list.items():
                    if household.human_capital > best_candidate_human_capital:
                        best_candidate_hhID = hhID

                if best_candidate_hhID != -1:
                    # check candidate falls within firm production function
                    labour_cost = np.mean(
                        self.households[best_candidate_hhID].expected_income)

                    for w in firm.workers.values():
                        labour_cost += np.mean(w.expected_income)
                    human_capital = (self.households[
                        best_candidate_hhID].human_capital * np.mean(
                        self.households[best_candidate_hhID].expected_income
                        )/labour_cost)
                    for w in firm.workers.values():
                        human_capital += w.human_capital * w.income/labour_cost

                    if (firm.expected_production/(firm.productivity
                                                  * firm.capital_stock
                                                  ** firm.capital_share)
                            > (human_capital**firm.human_capital_share)
                            * labour_cost**firm.labour_share):
                        firm.workers[best_candidate_hhID] = self.households[
                            best_candidate_hhID]

                        self.households[best_candidate_hhID].life_stage = 'E'
                        hiring = True

    def get_income_per_capita(self):
        """
        Calculate income per capita.

        Used to determine appropriate level of government welfare spending.
        """
        total_income = 0
        for h in self.households.values():
            total_income += h.income
        total_unemployed = len(self.get_unemployed().keys())
        total_employed = len(self.households.keys()) - total_unemployed
        if total_employed == 0:
            income_per_capita = 0
        else:
            income_per_capita = total_income/total_employed
        return income_per_capita

    def move_production_to_inventory(self):
        for f in self.firms.values():
            f.inventory += f.production
            f.expected_production = f.production
            f.production = 0

    def consumption_market(self):
        # Cycle through every household's spending.
        # randomly assign 10% of spending to random firm
        # if firm has no inventory, reallocate
        for hhID, household in self.households.items():
            household.update_consumption()

            # Cycle through each product in household's spending basket
            for household_product in household.spending_basket:
                product_spending = (household.spending
                                    * household_product['Proportion'])
                random.shuffle(self.products[household_product['Name']])
                while product_spending > 0:

                    # Cycle though list of firms that makes product
                    for firmID in self.products[household_product['Name']]:
                        if household_product['Price'] >= self.firms[
                                firmID].product_price:
                            quantity = product_spending/self.firms[
                                firmID].product_price
                            sales = self.firms[firmID].update_revenue(quantity)
                            product_spending -= sales

                        if product_spending == 0:
                            # spent all expected spending
                            break

                    if product_spending > 0:  # household still wants to spend
                        household_product['Price'] *= 1.03

                    # check if firms are all out of stock
                    out_of_stock = 1
                    for firmID in self.products[household_product['Name']]:
                        if self.firms[firmID].inventory > 0:
                            out_of_stock = 0
                    if out_of_stock:
                        household.spending -= product_spending
                        break

    def calculate_CPI(self):
        total_revenue = 0
        total_production = 0
        for firmID, firm in self.firms.items():
            total_revenue += firm.revenue
            total_production += firm.revenue/firm.product_price

        self.CPI = total_revenue/total_production

    def calculate_GDP(self):
        GDP = 0
        for f in self.firms.values():
            GDP += f.revenue
            GDP += f.inventory * f.product_price

        self.GDP = GDP
        return GDP
    # update economy data (c)

    def financial_market(self):
        """
        Adjust household/firm/government asset allocation.

        Household savings receive interest. Firms pay interest on debt,
        calculate profit and invest in capital based on that as well as
        interest rates and inflation. Government also recieves/pays interest.

        This function will be expanded as asset markets are developed in
        Kuznets.

        """
        for h in self.households.values():
            h.update_financial(self.interest_rate)
        for f in self.firms.values():
            profit = f.update_financial(self.interest_rate + 0.02,
                                        self.growth_rate(
                                            self.economy_data['CPI']))
            if profit > 0:  # company tax
                self.government.revenue += (profit
                                            * self.government.corporate_tax)
                f.debt += profit * self.government.corporate_tax
        self.government.update_financial(self.interest_rate)

    # update economy data (f)

    def update_households_data(self, households_data, households, time, cycle):
        """Add latest data to household dataframe."""
        new_data = [pd.DataFrame({
            'Human capital': float(household.human_capital),
            'Expected income': np.mean(household.expected_income),
            'Income': float(household.income),
            'Life stage': str(household.life_stage),
            'Spending': float(household.spending),
            'Savings': float(household.savings), },
            index=[(time, cycle, hhID)])
                for hhID, household in households.items()]
        new_households_data = [households_data] + new_data

        return new_households_data

    def update_firms_data(self, firms_data, firms, time, cycle):
        """Add latest data to firms dataframe."""
        new_data = [pd.DataFrame({
            'Expected production': float(firm.expected_production),
            'Production': float(firm.production),
            'Product price': float(firm.product_price),
            'Revenue': float(firm.revenue),
            'Inventory': float(firm.inventory),
            'Labour cost': float(firm.labour_cost),
            'Workers': int(len(firm.workers.keys())),
            'Capital investment': float(firm.capital_investment),
            'Capital stock': float(firm.capital_stock),
            'Marginal cost': float(firm.marginal_cost),
            'Debt': float(firm.debt),
            'Profit': float(firm.profit),
            },
            index=[(self.time, cycle, firmID)])
                for firmID, firm in self.firms.items()]

        new_firms_data = [firms_data] + new_data
        return new_firms_data

    def accounting_pre(self):
        """
        Various accounting before dataframe storage.

        Household savings are adjusted for spending/saving.
        Firm debt adjusted for labour spending/revenue.
        Government debt adjusted for expenditure/revenue.
        """
        for h in self.households.values():
            h.savings += h.income - h.spending
        for f in self.firms.values():
            f.debt += f.labour_cost
            f.debt -= f.revenue
        self.government.debt += (self.government.expenditure
                                 - self.government.revenue)

    def update_economy_data(self, cycle):
        self.accounting_pre()

        """ self.households_data = pd.concat(
            updateeconomydata.update_households_data(self.households_data,
            self.households, self.time, cycle))"""
        self.households_data = pd.concat(
            self.update_households_data(self.households_data, self.households,
                                        self.time, cycle))

        """ self.firms_data = pd.concat(updateeconomydata.update_firms_data(
            self.firms_data, self.firms, self.time, cycle))"""
        self.firms_data = pd.concat(self.update_firms_data(self.firms_data,
                                    self.firms, self.time, cycle))

        self.government_data = pd.concat([
            self.government_data,
            pd.DataFrame({
                'Revenue': float(self.government.revenue),
                'Expenditure': float(self.government.expenditure),
                'Debt': float(self.government.debt)
                }, index=[(self.time, cycle)])
            ])

        df1 = self.households_data.xs(cycle, level='cycle').groupby(
            level=0).sum().loc[self.time]
        df2 = self.firms_data.xs(cycle, level='cycle').groupby(
            level=0).sum().loc[self.time]
        """ df3 = self.government_data.xs(cycle, level='cycle').groupby(
            level=0).sum().loc[self.time]"""

        sum = pd.DataFrame({
            'Household income': float(df1['Income']),
            'Household savings': float(df1['Savings']),
            'Household spending': float(df1['Spending']),
            'Household expected income':
                float(np.mean(df1['Expected income'])),
            'Firm inventory': float(df2['Inventory']),
            'Firm production': float(df2['Production']),
            'Firm revenue': float(df2['Revenue']),
            'Firm debt': float(df2['Debt']),
            'Firm profit': float(df2['Profit']),
            'CPI': float(self.CPI),
            'Interest rate': float(self.interest_rate),
            'Unemployment rate':
                float(len(self.get_unemployed().keys())/len(
                    self.households.keys())),
            }, index=[(self.time, cycle)])

        self.economy_data = pd.concat([self.economy_data, sum], sort=False)
        self.accounting_post()

    def accounting_post(self):
        """
        Various accounting after dataframe storage.

        Household income/spending reset to zero.
        Firm labour spending/revenue/capital investment/profit reset to zero.
        Government expenditure/revenue reset to zero.
        """
        for h in self.households.values():
            h.income = 0
            h.spending = 0
        for f in self.firms.values():
            f.capital_investment = 0
            f.labour_cost = 0
            f.revenue = 0
            f.profit = 0
        self.government.expenditure = 0
        self.government.revenue = 0

    def demographics(self):
        """
        Adjust household demographics.

        Placeholder function for now, will eventually allow for household
        aging, household entry/exits.

        """
        number_households = len(self.households.keys())
        return number_households

    def production_cycle(self):
        """
        Production.

        First phase of economic cycle.

        Begin with labor market churn: firms decide on their profit-maximising
        production and then lower or increase their labour force to try and
        meet their production goals.

        Next is actual production, then household taxes, then welfare.

        Final step is households update their future income expectations.
        """
        for f in self.firms.values():
            f.update_expected_production(
                self.growth_rate(self.economy_data['CPI']))
        self.worker_seperations()
        self.worker_hiring()

        for f in self.firms.values():
            f.update_production()
            f.get_marginal_cost(self.growth_rate(self.economy_data['CPI']))  # move financial?

        self.government.income_tax(self.households)
        self.government.welfare(
            self.get_income_per_capita(),
            self.get_unemployed())

        for h in self.households.values():
            h.update_income_expectations(
                self.growth_rate(self.economy_data['CPI']),
                self.government.income_tax_rate)

    def consumption_cycle(self):
        self.move_production_to_inventory()
        self.consumption_market()
        self.calculate_CPI()

    def financial_cycle(self):
        self.financial_market()

    def cycle(self, number=1):
        # start = time.time()
        for i in range(number):
            self.update_time()
            self.production_cycle()
            self.update_economy_data('p')
            self.consumption_cycle()
            self.update_economy_data('c')
            self.financial_cycle()
            self.update_economy_data('f')
            self.demographics()
            # self.status()

        # end = time.time()
        # print('time ' + str(round(end - start,2)))
        self.print_households_data(-1)
        self.print_firms_data(-1)
        # self.print_government_data(-1)
        self.print_all()

    def get_unemployed(self):
        """Return dict of unemployed households."""
        unemployed = {}
        for hhID, household in self.households.items():
            if household.life_stage == 'U':
                unemployed[hhID] = household
        return unemployed

    def get_production_cycle_data(self):
        """Return dataframe of data captured in production cycle."""
        return self.economy_data.iloc[::3, ]

    def get_consumption_cycle_data(self):
        """Return dataframe of data captured in consumption cycle."""
        return self.economy_data.iloc[1::3, ]

    def get_financial_cycle_data(self):
        """Return dataframe of data captured in financial cycle."""
        return self.economy_data.iloc[2::3, ]

    def household_add(self):
        print("Household add")

    def household_remove(self, hhID):
        # del self.household(hhID)
        pass

    def firm_add(self):
        print("Firm add")

    def firm_remove(self, firmID):
        print("Firm remove")

    def print_economy_data(self, time):
        if time == -1:
            print(self.economy_data.to_string())
        else:
            print(self.economy_data.loc[(time,):(time,)])

    def print_households_data(self, time):
        if time == -1:
            print(self.households_data.to_string())
            # print(self.households_data.xs(1, level=2, drop_level=False))
        else:
            print(self.households_data.loc[(time,):(time,)])

    def print_firms_data(self, time):
        """Print firm dataframe.

        If time is -1 it will print the entire dataframe.
        """
        if time == -1:
            print(self.firms_data.to_string())
            # print(self.firms_data.xs(1, level=2, drop_level=False))
        else:
            print(self.firms_data.loc[(time,):(time,)])

    def print_government_data(self, time):
        if time == -1:
            print(self.government_data.to_string())
        else:
            print(self.government_data.loc[(time,):(time,)])

    def print_labour_market(self):
        print("Labour market allocation to firms:")
        for firmID, firm in self.firms.items():
            print("Firm ID: " + str(firmID) + " " + str(firm.workers.keys()))
        print("Unemployed: " + str(self.get_unemployed().keys()))

    def update_time(self):
        self.time += 1
        print("Time is: " + str(self.time))

    def growth_rate(self, series):
        if self.time == 0:
            return 0
        try:
            return series[-1]/series[-4]
        except IndexError:
            return 0

    def status(self):
        self.print_households_data(self.time)
        self.print_firms_data(self.time)
        self.print_government_data(self.time)
        self.print_economy_data(self.time)

    def print_all(self):
        print(self.economy_data.to_string())
