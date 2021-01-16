import pandas as pd
import numpy as np
import sympy
from fractions import Fraction
import re
import os

from chemlib.utils import DimensionalAnalyzer, reduce_list

this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "resources", "PTE_updated.csv")

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
AVOGADROS_NUMBER = 6.02e+23

def parse_formula(formula : str) -> dict: # Formula Parsing by Aditya Matam
    def multiply(formula: dict, mul: int) -> None:
        for key in formula: formula[key] *= mul

    formDict = {}
    # PARENS
    for match in re.finditer(r"\((.*?)\)(\d*)", formula):
        parens = parse_formula(match.group(1))
        mul = match.group(2)
        if not mul: mul = 1
        multiply(parens, int(mul))
        formDict.update(parens)
    # REST
    for match in re.finditer(r"(\(?)([A-Z][a-z]?)(\d*)(\)?)", formula):
        left, elem, mul, right = match.groups()
        if left or right: continue
        if not mul: mul = 1
        if elem in formDict:
            formDict[elem] += int(mul)
        else:
            formDict[elem] = int(mul)

    return formDict

class PeriodicTable(pd.DataFrame):
    """
    A ``pandas.Dataframe`` object that contains periodic table data:
    
        >>> import chemlib
        >>> chemlib.PeriodicTable()
            Unnamed: 0  AtomicNumber  ...                  Config MassNumber
        0             0           1.0  ...                     1s1        1.0
        1             1           2.0  ...                     1s2        4.0
        2             2           3.0  ...                [He] 2s1        7.0
        3             3           4.0  ...                [He] 2s2        9.0
        4             4           5.0  ...            [He] 2s2 2p1       11.0
        ..          ...           ...  ...                     ...        ...
        113         113         114.0  ...  [Rn] 5f14 6d10 7s2 7p2      289.0
        114         114         115.0  ...  [Rn] 5f14 6d10 7s2 7p3      288.0
        115         115         116.0  ...  [Rn] 5f14 6d10 7s2 7p4      292.0
        116         116         117.0  ...  [Rn] 5f14 6d10 7s2 7p5      295.0
        117         117         118.0  ...  [Rn] 5f14 6d10 7s2 7p6      294.0
        [118 rows x 31 columns]
    """

    def __init__(self, *args, **kwargs):
        super(PeriodicTable, self).__init__(pd.read_csv(DATA_PATH))
        
    def get_element_properties_from_symbol(self, symbol):
        # values = np.array(self.iloc[[self.index[self['Symbol'] == symbol].tolist()[0]]]).ravel()
        # keys = list(self)
        # return dict(zip(keys, values))
        series = self.loc[self["Symbol"] == symbol].iloc[0]
        return series.to_dict()

pte = PeriodicTable()

class Element:
    """
    A class containing all the properties of an element:
    """
    
    def __init__(self, symbol): 
        self.properties = pte.get_element_properties_from_symbol(symbol)
        for key in self.properties:
            setattr(self, key, self.properties[key])
    
    def __getitem__(self, key: str):
        return self.properties[key]

    def __str__(self):
        return self["Symbol"]

class Compound:
    """
    Represents a chemical compound.
    """

    def __init__(self, formula):
        # self.atom_list = []
        # for i in self.occurences:
        #     for j in range(int(self.occurences[i])): 
        #         self.atom_list.append(i)
        # self.types = list(self.occurences.keys())
        # self.formula = list(zip(self.types, [self.atom_list.count(i) for i in self.types]))
        # self.formula = sum([[i[0], i[1]] for i in self.formula], [])
        # self.formula = (''.join([str(i) for i in self.formula])).translate(SUB)
        # self.formula = ""
        # self.elements = [Element(i) for i in self.atom_list]
        self.occurences = parse_formula(formula)
        self.elements = []
        self.formula = []
        for symbol in self.occurences:
            count = self.occurences[symbol]
            self.formula.append(f"{symbol}{count}")
            for _ in range(count):
                self.elements.append(Element(symbol))
        self.formula = ''.join(self.formula).translate(SUB)

    def __str__(self) -> str:
        return self.formula

    def molar_mass(self) -> float:
        mass = 0
        for element in self.elements:
            mass += element.AtomicMass
        return round(mass, 2)

    def percentage_by_mass(self, element) -> float:
        return round(((self.occurences[element] * Element(element).AtomicMass) / self.molar_mass()) * 100, 3)

    def oxidation_numbers(self) -> dict:
        if len(self.types) == 1:
            return 0
        
        ox_nums = {}
        
        def current() -> int:
            chrg = 0
            for sym in ox_nums:
                chrg += ox_nums[sym]*self.occurences[sym]
            return chrg

        table = {"F": -1, "O": -2}
        syms = list(self.occurences.keys())
        left = [i for i in syms]
        for sym in syms:
            if sym in table:
                ox_nums.update(**{sym: table[sym]})
                left.remove(sym)
            if int(Element(sym).Group) < 3:
                ox_nums.update(**{sym: int(Element(sym).Group)})
                left.remove(sym)
        
        if len(left) > 1:
            raise NotImplementedError
        
        ox_nums[left[0]] = int(-current()/self.occurences[left[0]])
        return ox_nums
    
    def get_amounts(self, **kwargs) -> dict:
        keys = kwargs.keys()

        if 'grams' not in keys and 'moles' not in keys and 'molecules' not in keys:
            raise TypeError('Expecting one argument: either grams= , moles= , or molecules=')

        if len(kwargs) > 1:
            raise TypeError(f"Got {len(kwargs)} arguments when expecting 1. Use either grams= , moles=, or molecules=")
        
        return DimensionalAnalyzer(
            grams = lambda moles: moles*self.molar_mass(),
            moles = lambda molecules: molecules/AVOGADROS_NUMBER,
            molecules = lambda grams: grams/self.molar_mass()*AVOGADROS_NUMBER
        ).plug(**kwargs)

class Reaction:
    def __init__(self, reactants: list, products: list):
        self.reinit(reactants, products)
    
    def __str__(self) -> str:
        return self.formula
    
    @classmethod
    def by_formula(cls, formula: str):
        reactants, products = formula.split('>')
        reactants = [Compound(f) for f in [i.strip(' -') for i in reactants.split('+')]]
        products = [Compound(f) for f in [i.strip(' -') for i in products.split('+')]]
        return cls(reactants, products)
    
    def reinit(self, reactants, products):
        self.reactants = reactants
        self.products = products
        self.compounds = self.reactants + self.products
        self.reactant_formulas = [reactant.formula for reactant in self.reactants]
        self.product_formulas = [product.formula for product in self.products]
        self.update_formula()

        self.reactant_occurences = {}
        self.product_occurences = {}

        for i in [self.reactants, self.products]:
            for reactant in i: 
                for key in reactant.occurences:
                    if i == self.reactants:
                        if not key in self.reactant_occurences:
                            self.reactant_occurences[key] = reactant.occurences[key]
                        else:
                            self.reactant_occurences[key] += reactant.occurences[key]
                    else:
                        if not key in self.product_occurences:
                            self.product_occurences[key] = reactant.occurences[key]
                        else:
                            self.product_occurences[key] += reactant.occurences[key]
                            
        if self.reactant_occurences == self.product_occurences:
            self.is_balanced = True
        else:
            self.is_balanced = False
        
    def update_formula(self) -> None:
        self.formula = []

        for i in self.reactants: self.formula.append(i.formula)
        self.formula.append(' --> ')
        for i in self.products: self.formula.append(i.formula)

        self.frequencies = {i:self.formula.count(i) for i in self.formula}
        self.constituents = list(dict.fromkeys(self.formula))

        self.formula = []
        for i in self.constituents:
            self.formula.append(str(self.frequencies[i]) + i)

        del self.frequencies[' --> ']
        self.constituents.remove(' --> ')

        self.formula = ' + '.join(self.formula).replace('+ 1 ', '').replace('  +', '')

    def balance(self):
        """Balances the Chemical Reaction
        :return: None
        :rtype: void
        """
        if not self.is_balanced:
            reference_vector = []
            seen_formulas = []
            for j in [self.reactants, self.products]:
                for compound in j:
                    for i in compound.elements:
                        if i.Symbol not in seen_formulas:
                            seen_formulas.append(i.Symbol)
                            reference_vector.append(i)

            compound_formulas = []
            compounds = []
            for j in [i for i in self.compounds]:
                if j.formula not in compound_formulas:
                    compound_formulas.append(j.formula)
                    compounds.append(j)

            matrix = []
            for compound in compounds:
                col = []
                for m in seen_formulas:
                    try:
                        if compound.formula in self.product_formulas:
                            col.append(-compound.occurences[m])
                        else:
                            col.append(compound.occurences[m])
                    except:
                        col.append(0)
                matrix.append(col)
            
            matrix = sympy.Matrix(np.array(matrix).transpose()).rref() #Row - echelon form
            solutions = list(np.array(matrix[0][:, -1].tolist() + [matrix[-1][-1]], dtype=np.object))
            solutions = np.array([[i] if type(i) is int else i for i in solutions]).ravel().astype(np.float)
            solutions = [abs(i) for i in solutions]
            denominators = [f.denominator for f in [Fraction(x).limit_denominator() for x in solutions]]
            solutions = [int(i*max(denominators)) for i in solutions]
            solutions[-1] = max(denominators)
            while 0 in solutions:
                solutions.remove(0)

            final_reactants = []
            final_products = []

            for sol in range(len(compounds)):
                if compounds[sol].formula in self.reactant_formulas:
                    final_reactants.append([compounds[sol]]*solutions[sol])

                if compounds[sol].formula in self.product_formulas:
                    final_products.append([compounds[sol]]*solutions[sol])
            
            final_reactants = sum(final_reactants, [])
            final_products = sum(final_products, [])

            self.reinit(final_reactants, final_products)

        else:
            return True

    def get_amounts(self, compound_number, **kwargs):
        """Gets Stoichiometric equivalents for all compounds in reaction from inputted grams, moles, or molecules.
        :param compound_number: The number of compound by order of appearance in the reaction.
        :type compound_number: int
        :raises TypeError: Expecting one argument: either grams= , moles= , or molecules=
        :return: Amounts of grams, moles, and molecules for each compound.
        :rtype: list
        """
        if not self.is_balanced:
            self.balance()

        keys = kwargs.keys()

        if 'grams' not in keys and 'moles' not in keys and 'molecules' not in keys:
            raise ValueError('Expecting one argument: either grams= , moles= , or molecules=')

        if len(kwargs) > 1:
            raise ValueError(f"Got {len(kwargs)} arguments when expecting 1. Use either grams= , moles=, or molecules=")

        seen_formulas = []
        compound_list = []
        for compound in self.compounds:
            if compound.formula not in seen_formulas:
                compound_list.append(compound)
            seen_formulas.append(compound.formula)
        
        if compound_number > len(compound_list) or compound_number < 1:
            raise ValueError(f"The reaction has {len(compound_list)} compounds. Please use a compound number between 1 and {len(compound_list)}, inclusive.")
        
        seen_set = []
        for formula in seen_formulas:
            if formula not in seen_set:
                seen_set.append(formula)

        compound_frequency = {i:seen_formulas.count(i) for i in seen_set}
        index_compound = compound_list[compound_number - 1]
        index_amounts = index_compound.get_amounts(**kwargs)
        index_moles = index_amounts['moles']
        index_multiplier = compound_frequency[index_compound.formula]
        multipliers = []

        for compound in compound_list:
            multiplier = compound_frequency[compound.formula]
            multipliers.append(multiplier/index_multiplier)
        
        amounts = []

        for i in range(len(compound_list)):
            amounts.append(compound_list[i].get_amounts(moles = index_moles*multipliers[i]))

        amounts[compound_number - 1] = index_amounts
        return amounts

    def limiting_reagent(self, *args, mode = 'grams'):
        if mode not in ['grams', 'molecules', 'moles']:
            raise ValueError("mode must be either grams, moles, or molecules. Default is grams")

        if not self.is_balanced: self.balance()

        reactants = []
        rformulas = []
        for i in self.reactants:
            if i.formula not in rformulas:
                rformulas.append(i.formula)
                reactants.append(i)

        if len(args) != len(reactants):
            raise TypeError(f"Expected {len(reactants)} arguments. The number of arguments should be equal to the number of reactants.")

        amounts = [reactants[i].get_amounts(**{mode: args[i]}) for i in range(len(args))]
        moles = [i['moles'] for i in amounts]
        eq_amounts = [self.get_amounts(i + 1, moles = moles[i]) for i in range(len(args))]
        data = [a[-1][mode.capitalize()] for a in eq_amounts]

        return (reactants[np.argmin(data)])

    def __str__(self):
        return self.formula

class Combustion(Reaction):

    def __init__(self, compound):
        if type(compound) is str:
            compound = Compound(compound)
        super().__init__(reactants=[compound, Compound("O2")], products=[Compound("H2O"), Compound("CO2")])
        self.balance()

class Solution:
    def __init__(self, solute: Compound, molarity: float):
        if type(solute) is Compound: self.solute = solute
        elif type(solute) is str: self.solute = Compound(solute)
        else: raise TypeError("solute must be either a string or a chemlib.chemistry.Compound object")
        self.molarity = molarity
    
    @classmethod
    def by_grams_per_liters(cls, solute: Compound, grams: float, liters: float):
        if type(solute) is Compound: cmpd = solute
        else: cmpd = Compound(solute)
        molarity = cmpd.get_amounts(grams = grams)["moles"] / liters
        return cls(solute, molarity)
    
    def get_amounts(self, **kwargs) -> dict:
        keys = kwargs.keys()

        if 'moles' not in keys and 'liters' not in keys and 'grams' not in keys:
            raise ValueError('Expecting one argument: either moles= , grams=, or liters=')

        if len(kwargs) != 1:
            raise ValueError(f"Got {len(kwargs)} arguments when expecting 1. Use either either moles= , grams=, or liters=")
        
        return DimensionalAnalyzer(
            moles = lambda liters: liters*self.molarity,
            liters = lambda grams: grams/self.solute.molar_mass()/self.molarity,
            grams = lambda moles: moles*self.solute.molar_mass()
        ).plug(**kwargs)

    def dilute(self, V1 = None, M2 = None, V2 = None, inplace = False) -> dict:
        if V1 is None:
            raise TypeError("You need to specify a starting volume of Solution in liters.")
        if V2 != None and M2 != None:
            raise TypeError("You can only specify one or the other, M2 or V2.")
            
        M1 = self.molarity #using function M1*V1 = M2*V2

        if M2 != None: V2 = M1*V1/M2
        elif V2 != None: M2 = M1*V1/V2

        if inplace == True: self.molarity = M2

        return {
            "Solute": self.solute.formula,
            "Molarity": round(M2, 4),
            "Volume": round(V2, 4)
        }

def empirical_formula_by_percent_comp(**kwargs):
    elems = list(kwargs.keys())
    percs = list(kwargs.values())
    if (sum(percs) != 100):
        raise ValueError("The sums of the percentages of the constituent elements must be equal to 100.")
    
    compounds = [Compound(elem) for elem in elems]
    moles = []
    for i in range(len(compounds)):
        moles.append((compounds[i].get_amounts(grams = percs[i]))['moles'])

    moles = [i/min(moles) for i in moles]
    moles = reduce_list(moles)
    final = [elems[i] + str(moles[i]) for i in range(len(moles))]
    
    return ("".join(final))
    
def combustion_analysis(CO2, H2O):
    molesC = Compound("CO2").get_amounts(grams = CO2)["moles"]
    molesH = (Compound("H2O").get_amounts(grams = H2O)['moles'])*2
    moles = reduce_list([molesC, molesH])
    moles = ["" if x == 1 else x for x in moles] #Remove all 1's
    return (f"C{moles[0]}H{moles[1]}")
    
if __name__ == '__main__':
    #print(pte)
    # b = Element('B')
    # print(b["FirstIonization"])
    # c = Compound("H2O")
    # print(c.get_amounts(grams = 25))
    # s = Solution(Compound("H2SO4"), 0.25)
    # print(s.get_amounts(moles = 5))

    r = Reaction.by_formula('H2 + O2 --> H2O')
    print(r)
    print(r.balance())
    print(r)
