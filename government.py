""" Class for all information about a government """

class Government():

    def __init__(self, settings):
        self.revenue = settings.init_govt_revenue # 0
        self.expenditure = settings.init_govt_expenditure # 0
        self.debt = settings.init_govt_debt # 0

        self.income_tax = 0.10
        self.unemployed = {}
        self.corporate_tax = 0.10


    def govt_production_taxation(self):
        pass

    def govt_consumption_taxation(self):
        pass

    def govt_spending(self):
        pass
