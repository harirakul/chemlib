import unittest

import sys
sys.path.insert(1, '../chemlib')

from chemlib.chemistry import Compound, Reaction

class TestBalancing(unittest.TestCase):

    #Balancing Equation Test Inputs
    EQUATIONS = [
        {
            "R": ['H2','O2'],
            "P": ['H2O'],
        },
        {
            "R": ['H6C6', 'O2'],
            "P": ['CO2','H2O'],
        },
        {
            "R": ['Na2S', 'HCl'],
            "P": ['NaCl','H2S'],
        },
    ]
    def test_balancing(self):
        for reaction in self.EQUATIONS:
            left = [Compound(i) for i in reaction['R']]
            right = [Compound(i) for i in reaction['P']]
            r = Reaction(left, right)
            r.balance()
            print(r)
            self.assertTrue(r.is_balanced)

if __name__ == "__main__":
    unittest.main()