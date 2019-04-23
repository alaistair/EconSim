""" Class for all information about a government """

class Government():

    def __init__(self, settings):
        self.revenue = settings.init_govt_revenue # 0
        self.expenditure = settings.init_govt_expenditure # 0
        self.debt = settings.init_govt_debt # 0

        self.income_tax = settings.init_income_tax #0.10
        self.corporate_tax = settings.init_corporate_tax # 0.10

    def govt_production_taxation(self):
        pass

    def govt_consumption_taxation(self):
        pass

    def govt_spending(self):
        pass

    def govt_financial(self, interest_rate):
        self.debt *= interest_rate
        return 1
