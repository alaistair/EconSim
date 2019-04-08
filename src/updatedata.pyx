import numpy as np
import pandas as pd

def update_households_data(households_data, cycle):

    new_households_data = [households_data] + [pd.DataFrame({'income':household.income,
        'savings':household.savings,
        'spending':household.spending,
        'expected income':np.mean(household.expected_income),
        'human capital':household.human_capital,},
        index = [(economy.time, cycle, hhID)]) for hhID, household in economy.households.items()]

    return pd.concat(new_households_data)
