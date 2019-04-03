class Settings():
    """ A class to store all settings for EconSim"""

    def __init__(self):

        # Initial economy settings. Households >= firms
        self.init_households = 200
        self.init_firms = 5
        self.init_interest_rate = 1.02
        self.init_unemployment_rate = 0.1

        # Initial household settings
        self.init_household_savings = 20
        self.init_MPC = 0.95
        self.init_human_capital = [10,20,30] # range of potential labour outputs

        # Initial firm settings
        self.init_production = int(15 * self.init_households / self.init_firms)
        self.init_labour_productivity = 1.05 # output per labour input
        self.init_capital_depreciation = 0.03 # capital stock depreciation per cycle

        # Initial government settings
        self.init_govt_revenue = 0
        self.init_govt_expenditure = 0
        self.init_govt_debt = 0
