from economy import Economy
import pygal
from pygal.style import DefaultStyle

econ = Economy(100)
econ.status()

def cycle(Economy):
    econ.consumption()
    print("\n")
    econ.status()
    econ.production()
    print("\n")
    econ.status()

for i in range(0, 20):
    cycle(econ)

chart = pygal.Line(style = DefaultStyle, x_label_rotation = 45, show_legend = True)
chart.title = 'EconSim'

chart.add('Production', econ.firms[0].production)
chart.add('Revenue', econ.firms[0].revenue)
chart.add('Inventory', econ.firms[0].inventory)
chart.add('Wages', econ.households[0].wages)
chart.add('Consumption', econ.households[0].consumption)
chart.add('Savings', econ.households[0].savings)
chart.render_to_file('python_repos.svg')
