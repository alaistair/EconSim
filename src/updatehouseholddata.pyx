from cpython cimport array
import numpy as np
import pandas as pd

cdef object cupdate_household_data(households_data, households, int time, str cycle):

    new_households_data = np.array([households_data], [pd.DataFrame({'income':float(household.income),
        'savings':float(household.savings),
        'spending':float(household.spending),
        'expected income':np.mean(household.expected_income),
        'human capital':float(household.human_capital),},
        index = [(time, cycle, hhID)]) for hhID, household in households.items()])

    return new_households_data

def update_household_data(households_data, households, int time, str cycle):
  return cupdate_household_data(households_data, households, time, cycle)
