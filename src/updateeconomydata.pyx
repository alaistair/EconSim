from cpython cimport array
import numpy as np
import pandas as pd

cdef object cupdate_households_data(households_data, households, int time, str cycle):
  new_households_data = [households_data] + [pd.DataFrame({'income':float(household.income),
    'savings':float(household.savings),
    'spending':float(household.spending),
    'expected income':np.mean(household.expected_income),
    'human capital':float(household.human_capital),},
    index = [(time, cycle, hhID)]) for hhID, household in households.items()]

  return new_households_data

cdef object cupdate_firms_data(firms_data, firms, int time, str cycle):
  new_firms_data = [firms_data] + [pd.DataFrame({'inventory':float(firm.inventory),
    'production':float(firm.production),
    'price':float(firm.product_price),
    'revenue':float(firm.revenue),
    'expected production':float(firm.expected_production),
    'capital investment':float(firm.capital_investment),
    'capital stock':float(firm.capital_stock),
    'debt':float(firm.debt),
    'debt/revenue':float(firm.debt/firm.revenue),
    'profit':float(firm.profit),
    'workers':int(len(firm.workers.keys()))},
    index = [(time, cycle, firmID)]) for firmID, firm in firms.items()]

  return new_firms_data

def update_households_data(households_data, households, int time, str cycle):
  return cupdate_households_data(households_data, households, time, cycle)

def update_firms_data(firms_data, firms, int time, str cycle):
  return cupdate_firms_data(firms_data, firms, time, cycle)
