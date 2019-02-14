class Settings():
    """ A class to store all settings for EconSim"""

    def __init__(self):

        # Initial economy settings
        self.init_households = 5
        self.init_firms = 5
        self.init_interest_rate = 1.03

        # Initial firm settings
        self.init_firm_expected_revenue = 100
        self.init_firm_debt = 3 * self.init_firm_expected_revenue
        self.init_productivity = 1.1 # output per input

        # Initial household settings
        self.init_savings = 100
        self.init_MPC = 0.9
