from __future__ import division
from collections import defaultdict
from household import Household
from firm import Firm
from government import Government
import random
import numpy as np
import pandas as pd
import time

class Economy():

    def __init__(self, settings):

        self.time = 0
        self.interest_rate = settings.init_interest_rate
        self.households = {} # dictionary of households
        self.firms = {} # dictionary of firms
        self.products = defaultdict(list)
        self.government = Government(settings)
        self.CPI = 1
        self.slow = 0

        # Initialise households
        tuples = [] # index (time, cycle, hhID) for household dataframe
        for i in range(0, settings.init_households):
            self.households[i] = Household(settings)
            tuples.append((self.time, 'p', i))

        # Initialise dataframe for household data
        self.households_data = pd.DataFrame({'income':[0.],
                                'savings':[0.],
                                'spending':[0.],
                                'human capital':[0.],
                                }, index = pd.MultiIndex.from_tuples(tuples, names=['time', 'cycle', 'hhID']))

        # Initialise firms
        tuples = [] # index (time, cycle, firmID) for firm dataframe
        for i in range(0, settings.init_firms):
            self.firms[i] = Firm(settings)
            tuples.append((self.time, 'p', i))

        # Initialise dataframe for firm data
        self.firms_data = pd.DataFrame({'inventory':[0.],
                                'production':[0.],
                                'price':[0.],
                                'revenue':[0.],
                                'debt':[0.]
                                }, index = pd.MultiIndex.from_tuples(tuples, names=['time', 'cycle', 'firmID']))

        # Initialise dataframe for government data
        tuples = [(self.time, 'p')]
        self.government_data = pd.DataFrame({'revenue':[0.],
                                'expenditure':[0.],
                                'debt':[0.]
                                }, index = pd.MultiIndex.from_tuples(tuples, names=['time', 'cycle']))

        # Initialise dataframe for economy data
        #tuples = []
        #tuples.append((self.time, 'p'))

        self.economy_data = pd.DataFrame({'Household income':[0.],
                                        'Household savings':[0.],
                                        'Household spending':[0.],
                                        'Firm inventory':[0.],
                                        'Firm production':[0.],
                                        'Firm revenue':[0.],
                                        'Firm debt':[0.],
                                        'Government revenue':[0.],
                                        'Government expenditure':[0.],
                                        'Government debt':[0.],
                                        'CPI':[0.],
                                        'Interest rate':[0.],
                                        'Unemployment rate':[0.],
                        }, index = pd.MultiIndex.from_tuples(tuples, names=['time', 'cycle']))

        # Who works where
        # Every firm gets at least on worker
        total_population = list(self.households.keys())
        for firmID, firm in self.firms.items():
            i = random.choice(total_population)
            firm.workers[i] = self.households[i]
            total_population.remove(i)

        # unemployed
        unemployed = total_population.pop()
        self.government.unemployed[unemployed] = self.households[unemployed]
        unemployed = total_population.pop()
        self.government.unemployed[unemployed] = self.households[unemployed]

        # allocate remaining workers
        for worker in total_population:
            i = random.choice(list(self.firms.keys()))
            self.firms[i].workers[worker] = self.households[worker]

        # allocate firms to product
        for firmID, firm in self.firms.items():
            self.products[firm.product_name].append(firmID)

        # Initial production
        for firmID, firm in self.firms.items():
            labour_cost = firm.production/firm.labour_productivity
            firm.debt += labour_cost
            wages_per_worker = labour_cost/len(firm.workers)
            for hhID, worker in firm.workers.items():
                self.households[hhID].household_production(wages_per_worker)

        self.income_tax()
        self.welfare()

        # update economy dataframe
        for hhID, household in self.households.items():
            self.households_data.loc[(self.time, 'p', hhID)] = {
                                'income':household.wages,
                                'savings':household.savings,
                                'spending':household.spending,
                                'human capital':household.human_capital}

        for firmID, firm in self.firms.items():
            self.firms_data.loc[(self.time, 'p', firmID)] = {
                                'inventory':firm.inventory,
                                'production':firm.production,
                                'price':firm.product_price,
                                'revenue':firm.revenue,
                                'debt':firm.debt,}

        self.government_data = pd.DataFrame({'revenue':[0.],
                                'expenditure':[0.],
                                'debt':[0.]
                                }, index = pd.MultiIndex.from_tuples(tuples, names=['time', 'cycle']))

        df1 = self.households_data.xs('p', level='cycle').groupby(level=0).sum().loc[self.time]
        df2 = self.firms_data.xs('p', level='cycle').groupby(level=0).sum().loc[self.time]
        df3 = self.government_data.xs('p', level='cycle').groupby(level=0).sum().loc[self.time]

        self.economy_data.loc[(self.time, 'p')] = {
                                    'Household income':float(df1['income']),
                                    'Household savings':float(df1['savings']),
                                    'Household spending':float(df1['spending']),
                                    'Firm inventory':float(df2['inventory']),
                                    'Firm production':float(df2['production']),
                                    'Firm revenue':float(df2['revenue']),
                                    'Firm debt':float(df2['debt']),
                                    'Government revenue':float(df3['revenue']),
                                    'Government expenditure':float(df3['expenditure']),
                                    'Government debt':float(df3['debt']),
                                    'CPI':float(self.CPI),
                                    'Interest rate':float(self.interest_rate),
                                    'Unemployment rate':float(len(self.government.unemployed)/len(self.households)),
                                    }

        self.move_production_to_inventory()
        self.consumption_market()
        self.company_tax()
        self.update_economy_data('c')
        self.financial_market()
        self.update_economy_data('f')

    def production_market(self):
        # Cycle through each firm's production
        # Each firm 'hires' labour to create production
        for firmID, firm in self.firms.items():
            expected_labour_cost = firm.firm_expected_production()
            expected_production = firm.expected_production
            # Firm's goal is to approximate expected_production, while keeping
            # labour costs at or below expectations
            # Worker's goal is to maximise wages over and above their human capital
            # endowments
            

            labour_cost = firm.firm_production()
            wages_per_worker = labour_cost/len(firm.workers)
            for hhID, worker in firm.workers.items():
                self.households[hhID].household_production(wages_per_worker)



    def income_tax(self):
        self.government.expenditure = 0
        for hhID, worker in self.households.items():
            self.government.revenue += worker.wages * self.government.income_tax
            worker.wages *= (1-self.government.income_tax)

    def welfare(self):
        self.government.expenditure = self.government.revenue * 2.4
        total_unemployed = len(self.government.unemployed.keys())
        spending = self.government.expenditure/total_unemployed
        for hhID, household in self.government.unemployed.items():
            household.wages = spending

    def move_production_to_inventory(self):
        for firm in self.firms.values():
            firm.inventory += firm.production
            firm.production = 0

    def consumption_market(self):
        # Cycle through every household's spending.
        # randomly assign 10% of spending to random firm
        # if firm has no inventory, reallocate
        total_quantity = 0
        total_sales = 0
        for hhID, household in self.households.items():
            household.household_consumption()

            # Cycle through each product in household's spending basket
            for household_product in household.spending_basket:
                spending = household.spending * household_product['Proportion']
                random.shuffle(self.products[household_product['Name']])
                count = 0
                total_sales += spending
                while spending > 0:
                    count += 1
                    # Cycle though list of firms that makes product
                    for firmID in self.products[household_product['Name']]:
                        if household_product['Price'] >= self.firms[firmID].product_price:
                            total_quantity += spending/self.firms[firmID].product_price
                            spending -= self.firms[firmID].firm_revenue(spending) # return fulfilled sales
                            total_quantity -= spending/self.firms[firmID].product_price

                        if spending == 0:
                            break
                    if spending > 0:
                        household_product['Price'] *= 1.03

                    # check if all firms are out of stock
                    out_of_stock = 1
                    for firmID in self.products[household_product['Name']]:
                        if self.firms[firmID].inventory > 0:
                            out_of_stock = 0
                    if out_of_stock:
                        household.savings += spending
                        household.spending -= spending
                        total_sales -= spending
                        break

        self.CPI = total_sales/total_quantity

    def company_tax(self):
        for firm in self.firms.values():
            self.government.revenue += firm.revenue * self.government.corporate_tax
            firm.revenue *= (1-self.government.corporate_tax)

    def financial_market(self):
        self.government.govt_financial(self.interest_rate)
        for h in self.households.values():
            h.savings *= self.government.seigniorage
            h.household_financial(self.interest_rate)
        for f in self.firms.values():
            f.firm_financial(self.interest_rate)

    def update_economy_data(self, cycle):
        for hhID, household in self.households.items():
            self.households_data = pd.concat([self.households_data,
                                    pd.DataFrame({'income':household.wages,
                                        'savings':household.savings,
                                        'spending':household.spending,
                                        'human capital':household.human_capital,},
                                        index = [(self.time, cycle, hhID)])])

        for firmID, firm in self.firms.items():
            self.firms_data = pd.concat([self.firms_data,
                                pd.DataFrame({'inventory':firm.inventory,
                                    'production':firm.production,
                                    'price':firm.product_price,
                                    'revenue':firm.revenue,
                                    'debt':firm.debt},
                                    index = [(self.time, cycle, firmID)])], sort=True)

        self.government_data = pd.concat([self.government_data,
                            pd.DataFrame({'revenue':float(self.government.revenue),
                                        'expenditure':float(self.government.expenditure),
                                        'debt':float(self.government.debt)},
                                        index = [(self.time, cycle)])])

        df1 = self.households_data.xs(cycle, level='cycle').groupby(level=0).sum().loc[self.time]
        df2 = self.firms_data.xs(cycle, level='cycle').groupby(level=0).sum().loc[self.time]
        df3 = self.government_data.xs(cycle, level='cycle').groupby(level=0).sum().loc[self.time]

        sum = pd.DataFrame({'Household income': float(df1['income']),
                            'Household savings': '{0:f}'.format(df1['savings']),
                            'Household spending': float(df1['spending']),
                            'Firm inventory': float(df2['inventory']),
                            'Firm production': float(df2['production']),
                            'Firm revenue': float(df2['revenue']),
                            'Firm debt': float(df2['debt']),
                            'Government revenue':float(df3['revenue']),
                            'Government expenditure':float(df3['expenditure']),
                            'Government debt':float(df3['debt']),
                            'CPI':float(self.CPI),
                            'Interest rate':float(self.interest_rate),
                            'Unemployment rate':float(len(self.government.unemployed)/len(self.households)),
                            },
                            index = [(self.time, cycle)])
        self.economy_data = pd.concat([self.economy_data, sum], sort=False)
        return 1

    def cycle(self, number = 1):
        for i in range(number):
            self.update_time()
            self.production_market()
            self.income_tax()
            self.welfare()
            self.update_economy_data('p')
            self.move_production_to_inventory()
            self.consumption_market()
            self.company_tax()
            self.update_economy_data('c')
            self.financial_market()
            self.update_economy_data('f')
            if self.slow: time.sleep(100)
            self.status()
        self.print_all()

    def get_production_cycle_data(self):
        return self.economy_data.iloc[::3,]

    def get_consumption_cycle_data(self):
        return self.economy_data.iloc[1::3,]

    def get_financial_cycle_data(self):
        return self.economy_data.iloc[2::3,]

    def household_add(self):
        print("Household add")

    def household_remove(self, hhID):
        #del self.household(hhID)
        pass

    def firm_add(self):
        print("Firm add")

    def firm_remove(self, firmID):
        print("Firm remove")

    def print_economy_data(self, time):
        print(self.economy_data.loc[(time,):(time,)])

    def print_households_data(self, time):
        print(self.households_data.loc[(time,):(time,)])

    def print_firms_data(self, time):
        print(self.firms_data.loc[(time,):(time,)])

    def print_government_data(self, time):
        print(self.government_data.loc[(time,):(time,)])

    def print_labour_market(self):
        for firmID, firm in self.firms.items():
            print(str(firmID) + " " + str(firm.workers.keys()))
        for hhID in self.government.unemployed.keys():
            print("Unemp: " + str(hhID))

    def update_time(self):
        self.time += 1
        print("Time is: " + str(self.time))

    def status(self):
        self.print_economy_data(self.time)
        self.print_households_data(self.time)
        self.print_firms_data(self.time)

    def print_all(self):
        print(self.economy_data)
