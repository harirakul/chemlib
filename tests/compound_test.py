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