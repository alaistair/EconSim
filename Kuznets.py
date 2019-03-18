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
import sys
import pygame

from settings import Settings
from economy import Economy
import numpy as np
import pandas as pd

#print("Time elapsed: " + str(time.time() - t_zero))
print("EconSim 0.1")

settings = Settings()
econ1 = Economy(settings)

pygame.init()

print("SPACE to advance cycle, q to quit")


for i in range(200):
    econ1.cycle()

"""
def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                econ1.cycle()
                econ1.status()

            elif event.key == pygame.K_q:
                sys.exit()

while True:
    check_events()
"""

econ1.status()
print(econ1.households_data.to_string())
print(econ1.firms_data.to_string())
print(econ1.economy_data.to_string())
#print(econ1.get_consumption_cycle_data().to_string())
#print(econ1.get_production_cycle_data().to_string())
#print(econ1.get_financial_cycle_data().to_string())

#print(econ1.economy_data.index)

#test = econ1.households_data.loc[(1901,):(1901,)] # return everything at time 1901
#test2 = econ1.households_data.xs(1901) # return everything at time 1901
#test = econ1.households_data.iloc[econ1.households_data.index.get_level_values('hhID') == 5] # return all values for hhID == 5
#print(test2)

# Graphs
graph = 0

if graph:
    from graphs import Bar_graph
    bar_graph = Bar_graph(econ1)
    bar_graph.app.run_server(debug=True)

if __name__ == '__main__':
    print('finished')
