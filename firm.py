""" Class for all information about an individual firm """

class Firm():

    def __init__(self, firmID):
        self.firmID = firmID

        self.inventory = 200 # stock of inventory
        self.production = 0 # production for one cycle
        self.revenue = 0 # revenue for one cycle

    def firm_production(self, revenue):
        self.production = revenue

        return self.production

    # Adds sales to firm's revenue.
    # Return 0 if sales fulfilled, return residual if inventory run out
    def firm_revenue(self, sales):
        if self.inventory > sales: # firm fulfils all sales
            self.inventory -= sales
            self.revenue += sales
            #print("spend " + str(sales) + " at firm" + str(self.get_firm_ID()))
            return 0
        elif self.inventory > 0: # firm partially fulfils order, returns unfilled amount
            self.revenue += sales
            sales -= self.inventory
            self.inventory = 0
            #print("spend " + str(sales) + " at firm" + str(self.get_firm_ID()) + " " + str(sales) + ' leftover')
            return sales
        elif self.inventory == 0: # firm out of stock, return sales
            #print("firm" + str(self.get_firm_ID()) + " out of stock")
            return sales

    def get_firm_data(self):
        data = {'firmID': self.firmID,
                'inventory': [self.inventory],
                'production': [self.production],
                'revenue': [self.revenue]}
        return data

    def get_firm_ID(self):
        return self.firmID
