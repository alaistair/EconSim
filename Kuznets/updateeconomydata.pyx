from cpython cimport array
import numpy as np
import pandas as pd

cdef object cupdate_households_data(households_data, households, int time, str cycle):
  new_households_data = [households_data] + [pd.DataFrame({'Human capital':float(household.human_capital),
  'Expected income':np.mean(household.expected_income),
  'Income':float(household.income),
  'Spending':float(household.spending),
  'Savings':float(household.savings),},
  index = [(time, cycle, hhID)]) for hhID, household in households.items()]

  return new_households_data

cdef object cupdate_firms_data(firms_data, firms, int time, str cycle):
  new_firms_data = [firms_data] + [pd.DataFrame({'Expected production':float(firm.expected_production),
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
  index = [(time, cycle, firmID)]) for firmID, firm in firms.items()]

  return new_firms_data

def update_households_data(households_data, households, int time, str cycle):
  return cupdate_households_data(households_data, households, time, cycle)

def update_firms_data(firms_data, firms, int time, str cycle):
  return cupdate_firms_data(firms_data, firms, time, cycle)
