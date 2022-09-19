import unittest

import sys
sys.path.insert(1, '../chemlib')

from chemlib.chemistry import Compound, empirical_formula_by_percent_comp

class CasePair:
    def __init__(self, param, expected):
        self.parameter = param 
        self.expected = expected 

class TestEmpiricalFormula(unittest.TestCase):
    TEST_CASES = [
        CasePair(
            { "C": 59.9, "H": 8.1, "O": 32.0 },
            "C5H8O2"
        ),
        CasePair(
            { "C": 24.8, "H": 2.0, "Cl": 73.2 },
            "CHCl"
        ),
        CasePair(
            { "C": 86, "H": 14 },
            "CH2"
        ),
        CasePair(
            { "C": 92.3, "H": 7.7 },
            "CH"
        ),
        CasePair(
            { "C": 67.9, "H": 5.70, "N": 26.4 },
            "C3H3N"
        ),
        CasePair(
            { "P": 43.64, "O": 56.36 },
            "P2O5"
        )
    ]

    def test_empirical_formula(self):
        for case in self.TEST_CASES:
            percs = empirical_formula_by_percent_comp(**case.parameter)
            final = Compound(case.expected)
            self.assertEqual(percs, final, msg=f"{percs} == {final}")

if __name__ == "__main__":
    unittest.main()