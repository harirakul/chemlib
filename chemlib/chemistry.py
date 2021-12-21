import pandas as pd
import numpy as np
import sympy
from fractions import Fraction
import re
import os
from typing import List, Dict

from chemlib.utils import DimensionalAnalyzer, reduce_list
from chemlib.constants import Kw, AVOGADROS_NUMBER

this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "resources", "PTE_updated.csv")

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

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

def get_formula_coefficient(formula: str) -> int:
    if not formula[0].isdigit():
        return 1
    match = re.match(r"\d+", formula)
    return match.group()

class PeriodicTable(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        super(PeriodicTable, self).__init__(pd.read_csv(DATA_PATH))
        
    def get_element_properties_from_symbol(self, symbol):
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

    def __init__(self, formula, coefficient=1):
        self.occurences = parse_formula(formula)
        self.element_counts = {}
        # self.elements = []
        self.formula = [] # list, eventually str
        for symbol in self.occurences:
            count = self.occurences[symbol]
            self.formula.append(f"{symbol}{count}")
            self.element_counts[Element(symbol)] = count
            # for _ in range(count):
                # self.elements.append(Element(symbol))
        self.formula = ''.join(self.formula).translate(SUB)
        self.coefficient = coefficient # if not self.formula[0].isdigit() else int(re.match(r'\d+', self.formula))

    def __str__(self) -> str:
        return f"{str(self.coefficient)}•{self.formula}"

    def set_coefficient(self, coeff: int):
        self.coefficient = coeff

    def molar_mass(self) -> float:
        mass = 0
        for element, count in self.element_counts.items():
            mass += (element.AtomicMass * count)
        return round(mass, 2)

    def percentage_by_mass(self, element: str) -> float:
        return round(((self.occurences[element] * Element(element).AtomicMass) / self.molar_mass()) * 100, 3)

    def oxidation_numbers(self) -> dict:
        if len(self.occurences.keys()) == 1:
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

class ReactionReal:
    def __init__(self, reactants: List[Compound], products: List[Compound]):
        # fields
        self.reactants = reactants
        self.products = products
        self.compounds = []
        self.balanced = False
        self.formula = ""
        self.__update()

    # secondary construction method
    @classmethod 
    def by_formula(cls, formula: str):
        reactants, products = formula.split('>')
        reactants = [Compound(f) for f in [i.strip(' -') for i in reactants.split('+')]]
        products = [Compound(f) for f in [i.strip(' -') for i in products.split('+')]]
        return cls(reactants, products)
    
    def __str__(self) -> str:
        return self.formula

    def is_balanced(self) -> bool:
        return self.balanced

    def balance(self):
        # get all unique elements, mark each with unique ID (dict)
            # length is number of rows
        # get total number of reactants and products 
            # number of cols
        
        unique_elements = set()
        for compound in self.reactants:
            unique_elements.update(compound.occurences.keys())
        unique_elements = list(unique_elements)
        element_IDs = {unique_elements[i]: i  for i in range(len(unique_elements))}
        # print(f"Element ID Map: {element_IDs}")
        matrix = sympy.zeros(
            len(unique_elements), len(self.reactants) + len(self.products)
        ) # row, col

        switch = 1
        colCounter = 0
        for comp_list in (self.reactants, self.products):           
            for compound in comp_list:
                for symbol, count in compound.occurences.items():
                    ID = element_IDs[symbol] # row
                    matrix[ID, colCounter] = count * switch
                colCounter += 1
            switch *= -1

        rowE = matrix.rref()[0] # may be erroneous, investigate pivot locations...       
        # dropping 0 trailing columns
        while True:
            lastCol = list(rowE.col(-1))
            if any(lastCol):
                break
            rowE.col_del(-1)

        # multiply each term by max quotient
        lastCol = list(rowE.col(-1))
        mul = max([fraction.q for fraction in lastCol])
        coeffs = [abs(n * mul) for n in lastCol]
        coeffs.append(mul)       
       
        self.__assign_coefficients(coeffs)
        self.__update()
        self.balanced = True

    def __assign_coefficients(self, coeffs: List[int]):
        coef_iter = iter(coeffs)
        for comp_list in (self.reactants, self.products):
            for compound in comp_list:
                try:
                    coeff_value = next(coef_iter)
                    compound.set_coefficient(coeff_value)
                except StopIteration:
                    return

    def __update(self):
        lhs = " + ".join([str(comp) for comp in self.reactants])
        rhs = " + ".join([str(comp) for comp in self.products])
        self.compounds = self.reactants + self.products
        self.formula = f"{lhs} --> {rhs}"


if __name__ == "__main__":
    # r = ReactionReal.by_formula(
    #     "MnS + As2Cr10O35 + H2SO4 --> HMnO4 + AsH3 + CrS3O12 + H2O"
    # )
    r = ReactionReal.by_formula(
        "H2 + C7H8O2 --> C6H6O1 + C1H4 + H2O1"
    )
    print(r)
    r.balance()
    print(r)
   


class Reaction:
    def __init__(self, reactants: list, products: list):
        self.reinit(reactants, products)
    
    def __str__(self) -> str:
        return self.formula
    
    @classmethod
    def by_formula(cls, formula: str):
        """Creates Reaction instance with equation written as string
        Example: H2 + O2 -> H2O
        :return: Reaction instance
        :rtype: Reaction
        """
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
                            
        self.balanced = (self.reactant_occurences == self.product_occurences)
        
    def update_formula(self) -> None:
        # self.formula = []
        # for i in self.reactants: self.formula.append(i.formula)
        # self.formula.append(' --> ')
        # for i in self.products: self.formula.append(i.formula)

        self.formula = self.reactant_formulas + [" --> "] + self.product_formulas

        self.coefficients = {i:self.formula.count(i) for i in self.formula}
        self.constituents = list(dict.fromkeys(self.formula))

        self.formula = []
        for i in self.constituents:
            self.formula.append(str(self.coefficients[i]) + i)

        del self.coefficients[' --> ']
        self.constituents.remove(' --> ')

        self.formula = ' + '.join(self.formula).replace('+ 1 ', '').replace('  +', '')

    def balance(self):
        """Balances the Chemical Reaction
        :return: None
        :rtype: void
        """
        if not self.balanced:
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
            solutions = matrix[0][:, -1]
            lcm = sympy.lcm([i.q for i in solutions])
            solutions = lcm * solutions
            solutions = list(solutions)
            solutions = [abs(i) for i in solutions]

            while 0 in solutions:
                solutions.remove(0)

            if(len(compounds) > len(solutions)):
                solutions.append(lcm)

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
            self.balanced = True

    def is_balanced(self):
        return self.balanced

    def get_amounts(self, compound_number, **kwargs):
        """Gets Stoichiometric equivalents for all compounds in reaction from inputted grams, moles, or molecules.
        :param compound_number: The number of compound by order of appearance in the reaction.
        :type compound_number: int
        :raises TypeError: Expecting one argument: either grams= , moles= , or molecules=
        :return: Amounts of grams, moles, and molecules for each compound.
        :rtype: list
        """
        if not self.balanced:
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

        if not self.balanced: self.balance()

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
        data = [a[-1][mode] for a in eq_amounts]

        return (reactants[np.argmin(data)])
    
    def equilibrium_concentrations(self, starting_conc: list, ending_conc: list, show_work = False) -> dict:
        # Error Handling
        if not self.balanced: self.balance()
        if (len(starting_conc) != len(ending_conc) != len(self.constituents)): raise ValueError
        if (any(i == None for i in starting_conc)): raise ValueError("All starting concentrations must be known.")
        if (all(i == None for i in ending_conc)): raise ValueError("At least one ending concentration must be known.")

        # Calculation
        new_ending = [i for i in ending_conc]
        for i in range(len(ending_conc)):
            if ending_conc[i] is not None:
                chosen = i;

        chosen_cmpd = self.constituents[chosen]
        conc_change = ending_conc[chosen] - starting_conc[chosen]
        multiplier = 1 if conc_change > 0 else -1
        Kc = 1

        for i in range(len(ending_conc)):
            cmpd = self.constituents[i]
            coefficient = self.coefficients[cmpd]
            if (i != chosen):
                m = -1 if cmpd in self.reactant_formulas else 1
                new_ending[i] = starting_conc[i] + conc_change*(coefficient/self.coefficients[chosen_cmpd])*m*multiplier

            if (cmpd in self.reactant_formulas):
                Kc *= 1/(new_ending[i]**coefficient)
            else: Kc *= (new_ending[i]**coefficient)
        
        if show_work: # For those AP Chemistry students 😉
            changes = []
            for i in range(len(self.constituents)):
                cmpd = self.constituents[i]
                leading = "+" if cmpd in self.product_formulas else "-"
                changes.append(leading + str(self.coefficients[cmpd]) + "x")

            data = [starting_conc, changes, ending_conc]

            rows = ['Starting Concentrations (M)', "Concentration Changes (M)", "Ending Concentrations (M)"]
            df = pd.DataFrame(data, columns=self.constituents, index=rows)

            print(df)

        d = dict(zip(self.constituents, new_ending))
        d.update({"Kc": Kc})
        return d


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

def pH(**kwargs) -> dict:
    if len(kwargs) > 1: 
        raise ValueError("Accepting only one parameter: either pH, pOH, H, or OH")
    
    if list(kwargs.keys())[0] not in ('pH', 'pOH', 'H', 'OH'):
        raise ValueError("Accepting either pH, pOH, H, or OH")

    d =  (DimensionalAnalyzer(
        pH = lambda pOH: 14 - pOH,
        pOH = lambda H: 14 + np.log10(H),
        H = lambda OH: Kw/OH,
        OH = lambda pH: 10 ** (-(14 - pH))
    ).plug(**kwargs))

    if (d['pH'] > 7): f = "basic"
    elif (d['pH'] < 7): f = "acidic"
    else: f = "neutral"
    
    d.update(acidity = f)
    return d

def empirical_formula_by_percent_comp(**kwargs) -> str:
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

# if __name__ == '__main__':
#     # r = Reaction.by_formula('H2 + I2 --> HI')
#     # r.balance()
#     # print(r)

#     # starting_conc=[1e-3, 2e-3, 0]
#     # ending_conc=[None, None, 1.87e-3]

#     # print(r.equilibrium_concentrations(starting_conc, ending_conc, show_work=True))

#     r = Reaction.by_formula('H2 + N2 --> NH3')
#     r.balance()
#     print(r.limiting_reagent(20, 40, mode = 'moles'))

#     print(pH(pH = 2))
