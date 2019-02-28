"""

Todo:
Household enter/exit
Firm enter/exit
Household consumption function
Firm production function
Asset market
Housing market
Human capital
Government
International trade

Front end
User login


"""

import time
t_zero = time.time()

from settings import Settings
from economy import Economy
import numpy as np
import pandas as pd

print("Time elapsed: " + str(time.time() - t_zero))

settings = Settings()
econ1 = Economy(settings)

for i in range(0, 10):
    econ1.cycle()

#print(econ1.get_consumption_cycle_data().to_string())
#print(econ1.get_production_cycle_data().to_string())
#print(econ1.get_financial_cycle_data().to_string())
print(econ1.economy_data.to_string())
econ1.print_households_data()
econ1.print_firms_data()
#econ1.print_government_data()
#print(econ1.economy_data.index)
#print(econ1.economy_data.get_level_values(1)=='time')

#test = households_data.loc[(1,):(1,)] # return everything at time 1
#test2 = households_data.xs(1) # return everything at time 1
#test = households_data.iloc[households_data.index.get_level_values('hhID') == 5] # return all values for hhID == 5


# Graphs
graph = 0

if graph:
    from graphs import Bar_graph
    bar_graph = Bar_graph(econ1)
    bar_graph.app.run_server(debug=True)

if __name__ == '__main__':
    print('finished')
