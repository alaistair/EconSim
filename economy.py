from __future__ import division
from household import Household
from firm import Firm
from random import randint
import numpy as np
import pandas as pd

class Economy():

    # Initialise economy
    def __init__(self, settings):

        self.time = 0
        self.interest_rate = settings.init_interest_rate

        # Initialise households
        self.max_hhID = 0
        self.households = [] # list of households
        tuples = [] # index (time, cycle, hhID) for household dataframe
        for i in range(0, settings.init_households):
            self.households.append(Household(self.max_hhID, settings))
            tuples.append((self.time, 'p', i))
            self.max_hhID += 1

        # Initialise dataframe for household data
        self.households_data = pd.DataFrame({'income': [0.],
                                'savings': [0.],
                                'spending': [0.]
                                }, index = pd.MultiIndex.from_tuples(tuples, names=['time', 'cycle', 'hhID']))

        # Initialise firms
        self.max_firmID = 0
        self.firms = [] # list of firms
        tuples = [] # index (time, cycle, firmID) for firm dataframe
        for i in range(0, settings.init_firms):
            self.firms.append(Firm(self.max_firmID, settings))
            tuples.append((self.time, 'p', i))
            self.max_firmID += 1

        # Initialise dataframe for firm data
        self.firms_data = pd.DataFrame({'inventory': [0.],
                                'production': [0.],
                                'revenue': [0.],
                                'capital': [0.],
                                'debt': [0.]
                                }, index = pd.MultiIndex.from_tuples(tuples, names=['time', 'cycle', 'firmID']))

        # Fill with initial household data
        for h in self.households:
            self.households_data.loc[(0, 'p', h.hhID)] = {
                                'income':h.wages,
                                'savings':h.savings,
                                'spending':h.spending,}

        # Fill with initial firm data
        for f in self.firms:
            self.firms_data.loc[(0, 'p', f.firmID)] = {
                                'inventory':f.inventory,
                                'production':f.production,
                                'revenue':f.revenue,
                                'capital':f.capital,
                                'debt':f.debt,}

        # Dataframe for economy data
        df1 = self.households_data.groupby(level=0).sum()
        df2 = self.firms_data.groupby(level=0).sum()
        tuples = []
        tuples.append((self.time, 'p'))

        self.economy_data = pd.DataFrame({'total hh income':[0.],
                                        'total hh savings':[0.],
                                        'total hh spending':[0.],
                                        'total firm inventory':[0.],
                                        'total firm production':[0.],
                                        'total firm revenue':[0.],
                                        'total firm capital':[0.],
                                        'total firm debt':[0.]
                        }, index = pd.MultiIndex.from_tuples(tuples, names=['time', 'cycle']))

        self.economy_data.loc[(0, 'p')] = {
                                    'total hh income':float(df1['income']),
                                    'total hh savings':float(df1['savings']),
                                    'total hh spending':float(df1['spending']),
                                    'total firm inventory':float(df2['inventory']),
                                    'total firm production':float(df2['production']),
                                    'total firm revenue':float(df2['revenue']),
                                    'total firm capital':float(df2['capital']),
                                    'total firm debt':float(df2['debt']),}

    def production_market(self):
        # cycle through each firm's production
        i = 0
        # Each firm 'hires' labour to create production
        for firm in self.firms:
            output = firm.firm_production(firm.expected_revenue)
            self.households[i].household_production(output)
            i += 1

    def consumption_market(self):
        for firm in self.firms:
            firm.inventory += firm.production
            firm.production = 0
        # cycle through every household's spending.
        # randomly assign 10% of spending to random firm
        # if firm has no inventory, reallocate
        for household in self.households:
            spending = household.household_consumption()
            auction = spending/10
            while spending > 0:
                spending -= auction
                i = randint(0, len(self.firms)-1)
                spending += self.firms[i].firm_revenue(auction)
                if spending < auction:
                    auction = spending

    def financial_market(self):
        for household in self.households:
            household.household_financial(self.interest_rate)
        for firm in self.firms:
            firm.firm_financial(self.interest_rate)

    def update_economy_data(self, cycle):
        for household in self.households:
            df = pd.DataFrame({'income':household.wages,
                            'savings':household.savings,
                            'spending':household.spending},
                            index = [(self.time, cycle, household.hhID)])
            self.households_data = pd.concat([self.households_data, df])

        for firm in self.firms:
            df = pd.DataFrame({'inventory':firm.inventory,
                            'production':firm.production,
                            'revenue':firm.revenue,
                            'capital':firm.capital,
                            'debt':firm.debt},
                            index = [(self.time, cycle, firm.firmID)])
            self.firms_data = pd.concat([self.firms_data, df])

        df1 = self.households_data.xs(cycle, level='cycle').groupby(level=0).sum().loc[self.time]
        df2 = self.firms_data.xs(cycle, level='cycle').groupby(level=0).sum().loc[self.time]

        sum = pd.DataFrame({'total hh income': float(df1['income']),
                            'total hh savings': float(df1['savings']),
                            'total hh spending': float(df1['spending']),
                            'total firm inventory': float(df2['inventory']),
                            'total firm production': float(df2['production']),
                            'total firm revenue': float(df2['revenue']),
                            'total firm capital': float(df2['capital']),
                            'total firm debt': float(df2['debt'])},
                            index = [(self.time, cycle)])
        self.economy_data = pd.concat([self.economy_data, sum])
        return 1

    def get_households_data(self):
        return self.households_data

    def get_firms_data(self):
        return self.firms_data

    def get_economy_data(self):
        return self.economy_data

    def get_economy_consumption_data(self):
        return self.economy_data.iloc[::2,]

    def get_economy_production_data(self):
        return self.economy_data.iloc[1::2,]

    def household_add(self):
        print("Household add")

    def household_remove(self):
        print("Household remove")

    def firm_add(self):
        print("Firm add")

    def firm_remove(self):
        print("Firm remove")

    def update_time(self):
        self.time += 1
