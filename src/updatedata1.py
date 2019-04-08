import numpy as np
import pandas as pd

def update_economy_data(economy, cycle):

    new_households_data = [economy.households_data] + [pd.DataFrame({'income':household.income,
        'savings':household.savings,
        'spending':household.spending,
        'expected income':np.mean(household.expected_income),
        'human capital':household.human_capital,},
        index = [(economy.time, cycle, hhID)]) for hhID, household in economy.households.items()]

    economy.households_data = pd.concat(new_households_data)

    new_firms_data = [economy.firms_data] + [pd.DataFrame({'inventory':firm.inventory,
        'production':firm.production,
        'price':firm.product_price,
        'revenue':firm.revenue,
        'expected production':firm.expected_production,
        'capital investment':firm.capital_investment,
        'capital stock':firm.capital_stock,
        'debt':firm.debt,},
        index = [(economy.time, cycle, firmID)]) for firmID, firm in economy.firms.items()]

    economy.firms_data = pd.concat(new_firms_data, sort=False)

    economy.government_data = pd.concat([economy.government_data,
                        pd.DataFrame({'revenue':float(economy.government.revenue),
                                    'expenditure':float(economy.government.expenditure),
                                    'debt':float(economy.government.debt)},
                                    index = [(economy.time, cycle)])])

    df1 = economy.households_data.xs(cycle, level='cycle').groupby(level=0).sum().loc[economy.time]
    df2 = economy.firms_data.xs(cycle, level='cycle').groupby(level=0).sum().loc[economy.time]
    df3 = economy.government_data.xs(cycle, level='cycle').groupby(level=0).sum().loc[economy.time]

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
                        'CPI':float(economy.CPI),
                        'Interest rate':float(economy.interest_rate),
                        'Unemployment rate':float(len(economy.government.unemployed)/len(economy.households)),
                        },
                        index = [(economy.time, cycle)])

    economy.economy_data = pd.concat([economy.economy_data, sum], sort=False)

    return economy
