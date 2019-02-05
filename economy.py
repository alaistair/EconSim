from household import Household
from firm import Firm
from random import randint
import numpy as np
import pandas as pd

class Economy():

    # Initialise economy
    def __init__(self, settings):

        self.time = 0

        # Initialise households
        self.max_hhID = 0
        self.households = [] # list of households
        tuples = [] # index (time, cycle, hhID) for household dataframe
        for i in range(0, settings.init_households):
            self.households.append(Household(self.max_hhID))
            tuples.append((self.time, 'c', i))
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
            self.firms.append(Firm(self.max_firmID))
            tuples.append((self.time, 'c', i))
            self.max_firmID += 1

        # Initialise dataframe for firm data
        self.firms_data = pd.DataFrame({'inventory': [0.],
                                'production': [0.],
                                'revenue': [0.]
                                }, index = pd.MultiIndex.from_tuples(tuples, names=['time', 'cycle', 'firmID']))

        #self.update_economy_data()
        #self.households_data = self.households_data.iloc[1:] # remove first blank row
        #self.firms_data = self.firms_data.iloc[1:] # remove first blank row
        #self.economy_data = self.economy_data.iloc[1:] # remove first blank row
        #self.households_data.drop(self.households_data.index[:1], inplace=True)

        # Fill with initial household data
        for household in self.households:
            data = household.get_household_data()
            self.households_data.loc[(0, 'p', household.get_household_ID())] = {
                                'income':data['income'][-1],
                                'savings':data['savings'][-1],
                                'spending':data['spending'][-1],}

        # Fill with initial firm data
        for firm in self.firms:
            data = firm.get_firm_data()
            self.firms_data.loc[(0, 'p', firm.get_firm_ID())] = {
                                'inventory':data['inventory'][-1],
                                'production':data['production'][-1],
                                'revenue':data['revenue'][-1],}

        # Dataframe for economy data
        df1 = self.households_data.groupby(level=0).sum()
        df2 = self.firms_data.groupby(level=0).sum()
        tuples = []
        tuples.append((self.time, 'c'))
        tuples.append((self.time, 'p'))

        self.economy_data = pd.DataFrame({'total hh income':[0.],
                                        'total hh savings':[0.],
                                        'total hh spending':[0.],
                                        'total firm inventory':[0.],
                                        'total firm production':[0.],
                                        'total firm revenue':[0.]
                        }, index = pd.MultiIndex.from_tuples(tuples, names=['time', 'cycle']))

        self.economy_data.loc[(0, 'p')] = {
                                    'total hh income':float(df1['income']),
                                    'total hh savings':float(df1['savings']),
                                    'total hh spending':float(df1['spending']),
                                    'total firm inventory':float(df2['inventory']),
                                    'total firm production':float(df2['production']),
                                    'total firm revenue':float(df2['revenue']),}


    def production_market(self):
        # cycle through each firm's production
        i = 0
        for firm in self.firms:
            output = firm.firm_production(firm.revenue)
            self.households[i].household_production(output)
            firm.revenue = 0
            i += 1

    def consumption_market(self):
        # cycle through every household's spending.
        # randomly assign 10% of spending to random firm
        # if firm has no inventory, reallocate
        for household in self.households:
            spending = household.household_consumption(household.wages)
            auction = spending/10
            while spending > 0:
                spending -= auction
                i = randint(0, 9)
                spending += self.firms[i].firm_revenue(auction)
                if spending < auction:
                    auction = spending

    def financial_market(self):
        pass

    def update_economy_data(self, cycle):

        for household in self.households:
            data = household.get_household_data()
            df = pd.DataFrame({'income':data['income'],
                            'savings':data['savings'],
                            'spending':data['spending']},
                            index = [(self.time, cycle, data['hhID'])])
            self.households_data = pd.concat([self.households_data, df])

        for firm in self.firms:
            data = firm.get_firm_data()
            df = pd.DataFrame({'inventory':data['inventory'],
                            'production':data['production'],
                            'revenue':data['revenue']},
                            index = [(self.time, cycle, data['firmID'])])
            self.firms_data = pd.concat([self.firms_data, df])

        df1 = self.households_data.groupby(level=0).sum().loc[self.time]
        df2 = self.firms_data.groupby(level=0).sum().loc[self.time]
        sum = pd.DataFrame({'total hh income': float(df1['income']),
                            'total hh savings': float(df1['savings']),
                            'total hh spending': float(df1['spending']),
                            'total firm inventory': float(df2['inventory']),
                            'total firm production': float(df2['production']),
                            'total firm revenue': float(df2['revenue'])},
                            index = [(self.time, cycle)])
        self.economy_data = pd.concat([self.economy_data, sum])
        return 1

    def get_households_data(self):
        return self.households_data

    def get_firms_data(self):
        return self.firms_data

    def get_economy_data(self):
        return self.economy_data

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
