import unittest

import sys
sys.path.insert(1, '../chemlib')

from chemlib.chemistry import Compound, Reaction, empirical_formula_by_percent_comp

class TestFormulae(unittest.TestCase):

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
    def test_formulae(self):
        for formula_str, formula_parsed in self.CMPDS.items():
            self.assertEqual(Compound(formula_str).occurences, formula_parsed, msg=formula_str)

if __name__ == "__main__":
    unittest.main()