from __future__ import division
from collections import defaultdict
from src.household import Household
from src.firm import Firm
from src.government import Government
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
        self.unemployment_rate = settings.init_unemployment_rate # 10%

        # Initialise households
        tuples = [] # index (time, cycle, hhID) for household dataframe
        for i in range(0, settings.init_households):
            self.households[i] = Household(settings)
            tuples.append((self.time, 'p', i))

        # Initialise dataframe for household data
        self.households_data = pd.DataFrame({'income':[0.],
                                'savings':[0.],
                                'spending':[0.],
                                'expected income':[0.],
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
                                'expected production':[0.],
                                'debt':[0.]
                                }, index = pd.MultiIndex.from_tuples(tuples, names=['time', 'cycle', 'firmID']))

        # Initialise dataframe for government data
        tuples = [(self.time, 'p')]
        self.government_data = pd.DataFrame({'revenue':[0.],
                                'expenditure':[0.],
                                'debt':[0.]
                                }, index = pd.MultiIndex.from_tuples(tuples, names=['time', 'cycle']))

        # Initialise dataframe for economy data
        self.economy_data = pd.DataFrame({'Household income':[0.],
                                        'Household savings':[0.],
                                        'Household spending':[0.],
                                        'Household expected income':[0.],
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

        # Initialise labour market
        # All households are unemployed at start of cycle
        for hhID, household in self.households.items():
            self.government.unemployed[hhID] = household

        # Every firm gets at least one worker
        for firmID, firm in self.firms.items():
            i = random.choice(list(self.government.unemployed.keys()))
            firm.workers[i] = self.government.unemployed[i]
            del self.government.unemployed[i]

        # Allocate remaining workers until ~ unemployment rate. At least one
        # household will be unemployed.
        while float(len(self.government.unemployed)/len(self.households)) > self.unemployment_rate:
            if len(self.government.unemployed) == 1:
                break
            i = random.choice(list(self.government.unemployed.keys()))
            j = random.choice(list(self.firms.keys()))
            self.firms[j].workers[i] = self.households[i]
            del self.government.unemployed[i]

        # allocate firms to product
        for firmID, firm in self.firms.items():
            self.products[firm.product_name].append(firmID)

        self.production_market()
        self.income_tax()
        self.welfare()

        # update economy dataframe
        for hhID, household in self.households.items():
            self.households_data.loc[(self.time, 'p', hhID)] = {
                                'income':household.wages,
                                'savings':household.savings,
                                'spending':household.spending,
                                'expected income':household.expected_wages,
                                'human capital':household.human_capital}

        for firmID, firm in self.firms.items():
            self.firms_data.loc[(self.time, 'p', firmID)] = {
                                'inventory':firm.inventory,
                                'production':firm.production,
                                'price':firm.product_price,
                                'revenue':firm.revenue,
                                'expected production':firm.expected_production,
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
                                    'Household expected income':float(df1['expected income']),
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
        self.print_labour_market()

    def labour_market(self):
        # Workforce seperations
        for firmID, firm in self.firms.items():

            # Randomly fire one person
            if bool(firm.workers):
                hhID, household = random.choice(list(firm.workers.items()))
                self.government.unemployed[hhID] = household
                del firm.workers[hhID]

            # Also fire least productive worker
            if bool(firm.workers):
                lowest_productive_hhID = next(iter(firm.workers))
                lowest_productive = firm.workers[lowest_productive_hhID].human_capital/firm.workers[lowest_productive_hhID].expected_wages
                for hhID, household in firm.workers.items():
                    hh_productivity = household.human_capital/household.expected_wages
                    if hh_productivity < lowest_productive:
                        lowest_productive = hh_productivity
                        lowest_productive_hhID = hhID
                self.government.unemployed[lowest_productive_hhID] = firm.workers[lowest_productive_hhID]
                del firm.workers[lowest_productive_hhID]

            # Most underpaid person quits
            if bool(firm.workers):
                pass

        # Cycle through each firm
        # Each firm 'hires' labour to create production
        for firmID, firm in self.firms.items():
            # Get how much more each firm expecting to spend on labour
            expected_additional_labour_spending = firm.update_hiring_intentions()
            #print('firm ' + str(firmID) + ' expected spending ' + str(expected_additional_labour_spending))

            # Firm uses '37% rule' to hire, ie picks best candidate from random
            # 37% subset of candidates
            while expected_additional_labour_spending > 0:
                if len(self.government.unemployed.keys()) <= 1:
                    break # already at lowest rate of unemployment

                candidates = int(0.37 * len(self.government.unemployed))
                if candidates < 1: candidates = 1 # at least one candidate in consideration

                candidate_list = {}
                for i in range(0, candidates):
                    candidate = random.choice(list(self.government.unemployed.keys()))
                    candidate_list[candidate] = self.government.unemployed[candidate]

                best_candidate = -1 # hhID
                best_candidate_productivity = -100
                for hhID, household in candidate_list.items():
                    if expected_additional_labour_spending == 0:
                        break
                    if expected_additional_labour_spending < household.expected_wages:
                        if bool(firm.workers): # firm has workers
                            continue
                        else:
                            expected_additional_labour_spending *= 1.05
                    worker_productivity = household.human_capital/household.expected_wages
                    if worker_productivity > best_candidate_productivity:
                        best_candidate = hhID
                        best_candidate_productivity = worker_productivity

                if best_candidate == -1:
                    expected_additional_labour_spending = 0
                else:
                    firm.workers[best_candidate] = self.government.unemployed[best_candidate]
                    expected_additional_labour_spending -= household.expected_wages
                    del candidate_list[best_candidate]
                    del self.government.unemployed[best_candidate]

        for hhID, household in self.government.unemployed.items():
            household.expected_wages *= 0.99
            household.human_capital *= 0.995
        #print('new labour market:')
        #self.print_labour_market()

    def production_market(self):
        for firmID, firm in self.firms.items():
            for hhID, household in firm.workers.items():
                household.update_production(household.expected_wages, self.growth_rate(self.economy_data['CPI']))
                firm.update_production(household.expected_wages)
                household.human_capital *= firm.labour_productivity

    def income_tax(self):
        self.government.expenditure = 0
        for h in self.households.values():
            self.government.revenue += h.wages * self.government.income_tax
            h.wages *= (1-self.government.income_tax)

    def welfare(self):
        self.government.expenditure = self.government.revenue * 2.4
        total_unemployed = len(self.government.unemployed.keys())
        if total_unemployed == 0:
            pass
        else:
            spending = self.government.expenditure/total_unemployed
            for hhID, household in self.government.unemployed.items():
                household.wages = spending

    def move_production_to_inventory(self):
        for f in self.firms.values():
            f.inventory += f.production
            f.production = 0

    def consumption_market(self):
        # Cycle through every household's spending.
        # randomly assign 10% of spending to random firm
        # if firm has no inventory, reallocate
        total_quantity = 0
        total_sales = 0
        for hhID, household in self.households.items():
            household.update_consumption()

            # Cycle through each product in household's spending basket
            for household_product in household.spending_basket:
                spending = household.spending * household_product['Proportion']
                random.shuffle(self.products[household_product['Name']])
                total_sales += spending
                while spending > 0:
                    # Cycle though list of firms that makes product
                    for firmID in self.products[household_product['Name']]:
                        if household_product['Price'] >= self.firms[firmID].product_price:
                            total_quantity += spending/self.firms[firmID].product_price
                            spending -= self.firms[firmID].update_revenue(spending) # return fulfilled sales
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

        if total_quantity != 0:
            self.CPI = total_sales/total_quantity
        else:
            self.CPI = float('NaN')

    def company_tax(self):
        for firm in self.firms.values():
            self.government.revenue += firm.revenue * self.government.corporate_tax
            firm.revenue *= (1-self.government.corporate_tax)

    def financial_market(self):
        self.government.govt_financial(self.interest_rate)
        for h in self.households.values():
            #h.savings *= self.government.seigniorage
            h.update_financial(self.interest_rate)
        for f in self.firms.values():
            f.update_financial(self.interest_rate + 0.02)

    def update_economy_data(self, cycle):

        new_households_data = [self.households_data] + [pd.DataFrame({'income':household.wages,
            'savings':household.savings,
            'spending':household.spending,
            'expected income':household.expected_wages,
            'human capital':household.human_capital,},
            index = [(self.time, cycle, hhID)]) for hhID, household in self.households.items()]

        self.households_data = pd.concat(new_households_data)

        new_firms_data = [self.firms_data] + [pd.DataFrame({'inventory':firm.inventory,
            'production':firm.production,
            'price':firm.product_price,
            'revenue':firm.revenue,
            'expected production':firm.expected_production,
            'debt':firm.debt},
            index = [(self.time, cycle, firmID)]) for firmID, firm in self.firms.items()]

        self.firms_data = pd.concat(new_firms_data, sort=True)

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
                            'Household expected income':float(df1['expected income']),
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

    def cycle(self, number = 1):
        for i in range(number):
            self.update_time()
            self.labour_market()
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
            #self.status()
            #self.print_labour_market()
        self.print_all()

    def get_production_cycle_data(self):
        return self.economy_data.iloc[::3,]

    def get_consumption_cycle_data(self):
        return self.economy_data.iloc[1::3,]

    def get_financial_cycle_data(self):
        return self.economy_data.iloc[2::3,]

    def get_CPI_growth(self):
        return self.economy_data['CPI']

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
        print("Labour market allocation to firms:")
        for firmID, firm in self.firms.items():
            print("Firm ID: " + str(firmID) + " " + str(firm.workers.keys()))
        print("Unemployed: " + str(self.government.unemployed.keys()))

    def update_time(self):
        self.time += 1
        print("Time is: " + str(self.time))

    def growth_rate(self, series):
        try:
            return series[-1]/series[-4]
        except IndexError:
            return 0

    def status(self):
        self.print_economy_data(self.time)
        self.print_households_data(self.time)
        self.print_firms_data(self.time)

    def print_all(self):
        print(self.economy_data)
