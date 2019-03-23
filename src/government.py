""" Class for all information about a government """

class Government():

    def __init__(self, settings):
        self.revenue = settings.init_govt_revenue # 0
        self.expenditure = settings.init_govt_expenditure # 0
        self.debt = settings.init_govt_debt # 0

        self.income_tax = 0.10
        self.unemployed = {}
        self.corporate_tax = 0.10
        self.seigniorage = 1.04

    def govt_production_taxation(self):
        pass

    def govt_consumption_taxation(self):
        pass

    def govt_spending(self):
        pass

    def govt_financial(self, interest_rate):
        self.debt *= interest_rate
        self.debt += (self.expenditure - self.revenue)
        self.revenue = 0
        #self.expenditure = 0
        return 1

    def status(self):
        status = "Revenue: " + str(round(self.revenue,2)) + " expenditure: " + str(round(self.expenditure,2)) + " debt: " + str(round(self.debt,2))
        return status
