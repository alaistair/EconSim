from __future__ import division
from collections import defaultdict
from src.household import Household
from src.firm import Firm
from src.government import Government
import random
import numpy as np
import pandas as pd
import time
import sys
from functools import reduce

import src.updateeconomydata as updateeconomydata

class Economy():

    def __init__(self, settings):
        self.time = int(0)
        self.interest_rate = settings.init_interest_rate
        self.products = defaultdict(list)
        self.CPI = 1
        self.unemployment_rate = settings.init_unemployment_rate # 10%

        # Initialise dictionary of households
        self.households = {i:Household(settings) for i in range(settings.init_households)}

        # Initialise dataframe for household data
        tuples = [(self.time, 'p', i) for i in range(settings.init_households)]
        self.households_data = pd.DataFrame({'Human capital':[0.],
                                'Expected income':[0.],
                                'Income':[0.],
                                'Spending':[0.],
                                'Savings':[0.],
                                }, index = pd.MultiIndex.from_tuples(tuples, names=['time', 'cycle', 'hhID']))

        # Initialise dictionary of firms
        self.firms = {i:Firm(settings) for i in range(settings.init_firms)} # dictionary of firms

        # Initialise dataframe for firm data
        tuples = [(self.time, 'p', i) for i in range(settings.init_firms)]
        self.firms_data = pd.DataFrame({'Expected production':[0.],
                                'Production':[0.],
                                'Product price':[0.],
                                'Revenue':[0.],
                                'Inventory':[0.],
                                'Capital investment':[0.],
                                'Capital stock':[0.],
                                'Debt':[0.],
                                'Debt/revenue':[0.],
                                'Profit':[0.],
                                'Workers':[0.],
                                }, index = pd.MultiIndex.from_tuples(tuples, names=['time', 'cycle', 'firmID']))

        # Initialise government
        self.government = Government(settings)

        # Initialise dataframe for government data
        tuples = [(self.time, 'p')]
        self.government_data = pd.DataFrame({'Revenue':[0.],
                                'Expenditure':[0.],
                                'Debt':[0.]
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
        self.update_household_income_expectations(1)
        self.accounting_pre()

        # update economy dataframe
        for hhID, household in self.households.items():
            self.households_data.loc[(self.time, 'p', hhID)] = {
                                'Human capital':household.human_capital,
                                'Expected income':np.mean(household.expected_income),
                                'Income':household.income,
                                'Spending':household.spending,
                                'Savings':household.savings,}

        for firmID, firm in self.firms.items():
            self.firms_data.loc[(self.time, 'p', firmID)] = {
                                'Expected production':firm.expected_production,
                                'Production':firm.production,
                                'Product price':firm.product_price,
                                'Revenue':firm.revenue,
                                'Inventory':firm.inventory,
                                'Capital investment':firm.capital_investment,
                                'Capital stock':firm.capital_stock,
                                'Debt':firm.debt,
                                'Debt/revenue':firm.debt/firm.revenue,
                                'Profit':firm.profit,
                                'Workers':len(firm.workers.keys())}

        self.government_data = pd.DataFrame({'Revenue':self.government.revenue,
                                'Expenditure':self.government.expenditure,
                                'Debt':self.government.debt,
                                }, index = pd.MultiIndex.from_tuples(tuples, names=['time', 'cycle']))

        df1 = self.households_data.xs('p', level='cycle').groupby(level=0).sum().loc[self.time]
        df2 = self.firms_data.xs('p', level='cycle').groupby(level=0).sum().loc[self.time]
        df3 = self.government_data.xs('p', level='cycle').groupby(level=0).sum().loc[self.time]

        self.economy_data.loc[(self.time, 'p')] = {
                                    'Household income':float(df1['Income']),
                                    'Household savings':float(df1['Savings']),
                                    'Household spending':float(df1['Spending']),
                                    'Household expected income':float(np.mean(df1['Expected income'])),
                                    'Firm inventory':float(df2['Inventory']),
                                    'Firm production':float(df2['Production']),
                                    'Firm revenue':float(df2['Revenue']),
                                    'Firm debt':float(df2['Debt']),
                                    'Government revenue':float(df3['Revenue']),
                                    'Government expenditure':float(df3['Expenditure']),
                                    'Government debt':float(df3['Debt']),
                                    'CPI':float(self.CPI),
                                    'Interest rate':float(self.interest_rate),
                                    'Unemployment rate':float(len(self.government.unemployed)/len(self.households)),
                                    }

        self.accounting_post()
        self.move_production_to_inventory()
        self.consumption_market()
        self.calculate_CPI()
        self.update_economy_data('c')
        self.financial_market()
        self.update_economy_data('f')

    def labour_market(self):
        # Workforce seperations
        for firmID, firm in self.firms.items():
            firm.update_expected_production()

            # One worker quits
            if len(firm.workers) > 1:
                hhID, household = random.choice(list(firm.workers.items()))
                self.government.unemployed[hhID] = household
                del firm.workers[hhID]

            # Also fire least productive worker
            if len(firm.workers) > 1:
                lowest_productive_hhID = next(iter(firm.workers))
                lowest_productive = firm.workers[lowest_productive_hhID].human_capital/np.mean(firm.workers[lowest_productive_hhID].expected_income)
                for hhID, household in firm.workers.items():
                    hh_productivity = household.human_capital/np.mean(household.expected_income)
                    if hh_productivity < lowest_productive:
                        lowest_productive = hh_productivity
                        lowest_productive_hhID = hhID
                self.government.unemployed[lowest_productive_hhID] = firm.workers[lowest_productive_hhID]
                del firm.workers[lowest_productive_hhID]

            expected_additional_labour_spending = firm.update_hiring_intentions(self.interest_rate)
            while expected_additional_labour_spending < 0: # keep firing
                if len(firm.workers) > 1:
                    hhID, household = random.choice(list(firm.workers.items()))
                    self.government.unemployed[hhID] = household
                    del firm.workers[hhID]
                else:
                    print('one worker left')
                    break

        # Workforce hiring. Each firm 'hires' labour to create production
        for firmID, firm in self.firms.items():
            # Get how much more each firm expecting to spend on labour
            expected_additional_labour_spending = firm.update_hiring_intentions(self.interest_rate)

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
                best_candidate_productivity = 0
                for hhID, household in candidate_list.items():
                    if expected_additional_labour_spending == 0:
                        break
                    if expected_additional_labour_spending < np.mean(household.expected_income):
                        expected_additional_labour_spending *= 1.05
                    worker_productivity = household.human_capital/np.mean(household.expected_income)
                    if worker_productivity > best_candidate_productivity:
                        best_candidate = hhID
                        best_candidate_productivity = worker_productivity

                firm.workers[best_candidate] = self.government.unemployed[best_candidate]
                del candidate_list[best_candidate]
                del self.government.unemployed[best_candidate]
                expected_additional_labour_spending -= np.mean(household.expected_income)

    def production_market(self):
        for f in self.firms.values():
            for h in f.workers.values():
                h.update_production(np.mean(h.expected_income))
                f.update_production(np.mean(h.expected_income))
                h.human_capital *= f.labour_productivity

            # cobb doug
            print('actual production ' + str(f.production))
            print('cobb doug ' + str((f.capital_stock ** 0.7) * (f.labour_cost ** (1-0.7))))

    def income_tax(self):
        for h in self.households.values():
            self.government.revenue += h.income * self.government.income_tax
            h.income *= (1-self.government.income_tax)

    def welfare(self):
        # Get average incomes
        total_income = 0
        for h in self.households.values():
            total_income += h.income

        total_unemployed = len(self.government.unemployed.keys())
        total_employed = len(self.households.keys()) - total_unemployed
        if total_employed == 0:
            income_per_household = 0
        else:
            income_per_household = total_income/total_employed

        welfare_per_household = 0.8 * income_per_household

        if total_unemployed == 0:
            pass
        else:
            for h in self.government.unemployed.values():
                h.income = welfare_per_household
                self.government.expenditure += welfare_per_household
                h.human_capital *= 0.995

    def update_household_income_expectations(self, CPI):
        if CPI < 1: CPI = 1 # sticky wage expectations
        for h in self.households.values():
            h.expected_income.pop(0)
            h.expected_income.append(h.income * CPI)

        return h.expected_income

    # update economy data (p)

    def move_production_to_inventory(self):
        for f in self.firms.values():
            f.inventory += f.production
            f.production = 0

    def consumption_market(self):
        # Cycle through every household's spending.
        # randomly assign 10% of spending to random firm
        # if firm has no inventory, reallocate
        for hhID, household in self.households.items():
            household.update_consumption()
            if household.savings < -100:
                print('hhID ' + str(hhID) + ' savings ' + str(household.savings) + ' income ' +
                    str(household.expected_income[-1]) + ' ex income ' + str(household.expected_income) +
                    ' MPC ' + str(household.MPC))
                print(self.households_data.xs(hhID, level=2, drop_level=False))

                self.status()
                sys.exit()

            # Cycle through each product in household's spending basket
            for household_product in household.spending_basket:
                product_spending = household.spending * household_product['Proportion']
                random.shuffle(self.products[household_product['Name']])
                while product_spending > 0:
                    # Cycle though list of firms that makes product
                    for firmID in self.products[household_product['Name']]:
                        if household_product['Price'] >= self.firms[firmID].product_price:
                            product_spending -= self.firms[firmID].update_revenue(product_spending) # return fulfilled sales

                        if product_spending == 0:
                            break
                    if product_spending > 0:
                        household_product['Price'] *= 1.03

                    # check if firms are all out of stock
                    out_of_stock = 1
                    for firmID in self.products[household_product['Name']]:
                        if self.firms[firmID].inventory > 0:
                            out_of_stock = 0
                    if out_of_stock:
                        print('hhid ' + str(hhID) + ' out of stock ' + str(product_spending) + ' savings ' + str(household.savings))
                        break

    def calculate_CPI(self):
        total_revenue = 0
        total_production = 0
        for firmID, firm in self.firms.items():
            total_revenue += firm.revenue
            total_production += firm.revenue/firm.product_price

        self.CPI = total_revenue/total_production

    # update economy data (c)

    def financial_market(self):
        for h in self.households.values():
            h.update_financial(self.interest_rate)
        for f in self.firms.values():
            profit = f.update_financial(self.interest_rate + 0.02, self.growth_rate(self.economy_data['CPI']))
            if profit > 0: # company tax
                self.government.revenue += profit * self.government.corporate_tax
                f.debt += profit * self.government.corporate_tax
        self.government.govt_financial(self.interest_rate)

    # update economy data (f)

    def update_households_data(self, households_data, households, time, cycle):
        new_data = [pd.DataFrame({'Human capital':float(household.human_capital),
            'Expected income':np.mean(household.expected_income),
            'Income':float(household.income),
            'Spending':float(household.spending),
            'Savings':float(household.savings),},
            index = [(time, cycle, hhID)]) for hhID, household in households.items()]
        new_households_data = [households_data] + new_data

        return new_households_data

    def update_firms_data(self, firms_data, firms, time, cycle):
        new_data = [pd.DataFrame({'Expected production':float(firm.expected_production),
            'Production':float(firm.production),
            'Product price':float(firm.product_price),
            'Revenue':float(firm.revenue),
            'Inventory':float(firm.inventory),
            'Capital investment':float(firm.capital_investment),
            'Capital stock':float(firm.capital_stock),
            'Debt':float(firm.debt),
            'Debt/revenue':float(firm.debt/firm.revenue),
            'Profit':float(firm.profit),
            'Workers':int(len(firm.workers.keys()))},
            index = [(self.time, cycle, firmID)]) for firmID, firm in self.firms.items()]

        new_firms_data = [firms_data] + new_data
        return new_firms_data

    def accounting_pre(self):
        for h in self.households.values():
            h.savings += h.income - h.spending

    def update_economy_data(self, cycle):
        self.accounting_pre()

        #self.households_data = pd.concat(updateeconomydata.update_households_data(self.households_data, self.households, self.time, cycle))
        self.households_data = pd.concat(self.update_households_data(self.households_data, self.households, self.time, cycle))

        #self.firms_data = pd.concat(updateeconomydata.update_firms_data(self.firms_data, self.firms, self.time, cycle))
        self.firms_data = pd.concat(self.update_firms_data(self.firms_data, self.firms, self.time, cycle))

        self.government_data = pd.concat([self.government_data,
                            pd.DataFrame({'Revenue':float(self.government.revenue),
                                        'Expenditure':float(self.government.expenditure),
                                        'Debt':float(self.government.debt)},
                                        index = [(self.time, cycle)])])

        df1 = self.households_data.xs(cycle, level='cycle').groupby(level=0).sum().loc[self.time]
        df2 = self.firms_data.xs(cycle, level='cycle').groupby(level=0).sum().loc[self.time]
        df3 = self.government_data.xs(cycle, level='cycle').groupby(level=0).sum().loc[self.time]

        sum = pd.DataFrame({'Household income':float(df1['Income']),
                            'Household savings':float(df1['Savings']),
                            'Household spending':float(df1['Spending']),
                            'Household expected income':float(np.mean(df1['Expected income'])),
                            'Firm inventory':float(df2['Inventory']),
                            'Firm production':float(df2['Production']),
                            'Firm revenue':float(df2['Revenue']),
                            'Firm debt':float(df2['Debt']),
                            'Government revenue':float(df3['Revenue']),
                            'Government expenditure':float(df3['Expenditure']),
                            'Government debt':float(df3['Debt']),
                            'CPI':float(self.CPI),
                            'Interest rate':float(self.interest_rate),
                            'Unemployment rate':float(len(self.government.unemployed)/len(self.households)),
                            },
                            index = [(self.time, cycle)])

        self.economy_data = pd.concat([self.economy_data, sum], sort=False)
        self.accounting_post()

    def accounting_post(self):
        for h in self.households.values():
            h.income = 0
            h.spending = 0
        for f in self.firms.values():
            f.capital_investment = 0
        self.government.debt += self.government.expenditure - self.government.revenue
        self.government.expenditure = 0
        self.government.revenue = 0

    def demographics(self):
        number_households = len(self.households.keys())


    def cycle(self, number = 1):
        start = time.time()
        for i in range(number):
            self.update_time()
            self.labour_market()
            self.production_market()
            self.income_tax()
            self.welfare()
            self.update_household_income_expectations(self.growth_rate(self.economy_data['CPI']))
            self.update_economy_data('p')
            self.move_production_to_inventory()
            self.consumption_market()
            self.calculate_CPI()
            self.update_economy_data('c')
            self.financial_market()
            self.update_economy_data('f')
            self.demographics()
            #self.status()

        end = time.time()
        #print('time ' + str(round(end - start,2)))
        self.print_households_data(-1)
        self.print_firms_data(-1)
        self.print_government_data(-1)
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
        if time == -1:
            print(self.economy_data.to_string())
        else:
            print(self.economy_data.loc[(time,):(time,)])

    def print_households_data(self, time):
        if time == -1:
            print(self.households_data.to_string())
            #print(self.households_data.xs(1, level=2, drop_level=False))
        else:
            print(self.households_data.loc[(time,):(time,)])

    def print_firms_data(self, time):
        if time == -1:
            print(self.firms_data.to_string())
            #print(self.firms_data.xs(1, level=2, drop_level=False))
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
        print("Unemployed: " + str(self.government.unemployed.keys()))

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
