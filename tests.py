import unittest
from household import Household
from firm import Firm
from economy import Economy
from settings import Settings

class householdTest(unittest.TestCase):

    def test_household_production(self):
        settings = Settings()
        householdtest = Household(settings)
        self.assertEqual(householdtest.household_production(100), 100)
        #self.assertEqual()

unittest.main()
