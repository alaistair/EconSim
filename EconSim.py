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

def cycle(Economy):
    econ1.update_time()
    econ1.consumption_market()
    econ1.update_economy_data('c')
    econ1.production_market()
    econ1.update_economy_data('p')
    econ1.financial_market()


print("Time elapsed: " + str(time.time() - t_zero))

for i in range(0, 2):
    cycle(econ1)
print("Time elapsed: " + str(time.time() - t_zero))

households_data = econ1.get_households_data()
firms_data = econ1.get_firms_data()
economy_data = econ1.get_economy_data()
print(households_data.to_string())
print(firms_data.to_string())
print(economy_data.to_string())
print("Time elapsed: " + str(time.time() - t_zero))

#test = households_data.loc[(1,):(1,)] # return everything at time 1
#test2 = households_data.xs(1) # return everything at time 1

#test = households_data.iloc[households_data.index.get_level_values('hhID') == 5] # return all values for hhID == 5

#print(test.to_string())
#print(test2.to_string())

# Graphs
#bar_graph = Bar_graph(households_data, firms_data)

if __name__ == '__main__':
    #bar_graph.app.run_server(debug=True)
    print('finished')
