import unittest

import sys
sys.path.insert(1, '../chemlib')

from chemlib.chemistry import Compound, Reaction

CMPDS = {
    "H2SO4": {"H": 2, "S": 1, "O": 4},
    "H2O": {'H': 2, 'O': 1},
    "C6H12O6": {"C": 6, "H": 12, "O": 6},
    "Al23": {"Al": 23},
    "MnO4": {"Mn" : 1, "O": 4},
    "Mg(SO4)2": {"Mg": 1, "S":2, "O":8},
    "(Al)3(SO4)2": {"Al": 3, "S":2, "O":8},
    "MnSMn": {"Mn": 2, "S":1},
    "C2H5OH": {"C": 2, "H": 6, "O": 1}
}

class TestFormulae(unittest.TestCase):

    def test_formulae(self):
        for formula in CMPDS:
            self.assertEqual(Compound(formula).occurences, CMPDS[formula], msg = formula)

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

class TestBalancing(unittest.TestCase):

    def test_balancing(self):
        for reaction in EQUATIONS:
            left = [Compound(i) for i in reaction['R']]
            right = [Compound(i) for i in reaction['P']]
            r = Reaction(left, right)
            r.balance()
            print(r)
            self.assertTrue(r.is_balanced)

if __name__ == "__main__":
    unittest.main()