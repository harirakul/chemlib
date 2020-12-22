import unittest
from chemlib.chemistry import Compound

CMPDS = {
    "H2SO4": {"H": 2, "S": 1, "O": 4},
    "H2O": {'H': 2, 'O': 1},
    "C6H12O6": {"C": 6, "H": 12, "O": 6},
    "Al23": {"Al": 23}
}

class TestFormulae(unittest.TestCase):

    def test_formulae(self):
        for formula in CMPDS:
            self.assertEqual(Compound(formula).occurences, CMPDS[formula], msg = formula)

if __name__ == "__main__":
    unittest.main()