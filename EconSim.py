import time
t_zero = time.time()

from settings import Settings
from economy import Economy
from graphs import Bar_graph
import numpy as np
import pandas as pd

print("Time elapsed: " + str(time.time() - t_zero))

settings = Settings()
econ1 = Economy(settings)
econ1.consumption_market()
econ1.update_economy_data('c')
econ1.financial_market()
econ1.update_economy_data('f')

def cycle(Economy):
    econ1.update_time()
    econ1.production_market()
    econ1.update_economy_data('p')
    econ1.consumption_market()
    econ1.update_economy_data('c')
    econ1.financial_market()
    econ1.update_economy_data('f')


for i in range(0, 20):
    cycle(econ1)
    pass

print(econ1.households_data.to_string())
print(econ1.firms_data.to_string())
print(econ1.economy_data.to_string())
#print(economy_data.index)

#test = households_data.loc[(1,):(1,)] # return everything at time 1
#test2 = households_data.xs(1) # return everything at time 1

#test = households_data.iloc[households_data.index.get_level_values('hhID') == 5] # return all values for hhID == 5
# Graphs
bar_graph = Bar_graph(econ1.households_data, econ1.firms_data, econ1.economy_data)

if __name__ == '__main__':
    bar_graph.app.run_server(debug=True)
    print('finished')
