import unittest
import sys

sys.path.append('..')
from src.household import Household
from src.firm import Firm
from src.economy import Economy
from src.settings import Settings

class householdTest(unittest.TestCase):

    def test_household_production(self):
        settings = Settings()
        household = Household(settings)
        household.expected_income = [10,10,10]
        self.assertEqual(household.update_production(100, 1), [10,10,100])
        self.assertEqual(household.update_production(100, 1.05), [10,10,105])
        self.assertEqual(household.update_production(0, 1.05), [10,10,0])
        self.assertEqual(household.update_production(-10, 1.05), [10,10,0])
        self.assertEqual(household.update_production(100, 0.5), [10,10,100])
        self.assertEqual(household.update_production(100, -0.5), [10,10,100])

unittest.main()
