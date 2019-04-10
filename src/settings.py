import numpy as np

class Settings():
    """ A class to store all settings for EconSim"""

    def __init__(self):

        # App settings


        # Initial economy settings. Households >= firms
        self.init_households = 80
        self.init_firms = 3
        self.init_interest_rate = 1.02
        self.init_unemployment_rate = 0.2
        self.init_population_growth = 1.01

        # Initial household settings
        self.init_household_savings = 20
        self.init_MPC = 0.95
        self.init_human_capital = [10,20,30] # range of potential labour outputs

        # Initial firm settings
        self.init_production = self.init_households * (1-self.init_unemployment_rate) * np.mean(self.init_human_capital) / self.init_firms
        self.init_labour_productivity = 1.05 # output per labour input
        self.init_capital_depreciation = 0.03 # capital stock depreciation per cycle

        # Initial government settings
        self.init_govt_revenue = 0
        self.init_govt_expenditure = 0
        self.init_govt_debt = 0
        self.init_income_tax = 0.10
        self.init_corporate_tax = 0.10
