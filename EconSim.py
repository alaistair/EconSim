from economy import Economy
import graphs

econ = Economy(100)
econ.status()

def cycle(Economy):
    econ.consumption_market()
#    print("\n")
#    econ.status()
    econ.production_market()
    print("\n")
    econ.status()
    print(econ.get_households_wages())

for i in range(0, 10):
    cycle(econ)



if __name__ == '__main__':
    graphs.app.run_server(debug=True)
