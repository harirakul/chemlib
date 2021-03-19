from chemlib.chemistry import Combustion, Compound, Reaction
from chemlib.utils import reduce_list

# TODO: TEMP IMPLEMENTATIONS, NEED TO CONSIDER ADDITIONAL METHODS/CALCULATIONS  
# INTERFACE?

def combustion_analysis(CO2, H2O) -> str:
    molesC = Compound("CO2").get_amounts(grams = CO2)["moles"]
    molesH = (Compound("H2O").get_amounts(grams = H2O)['moles'])*2
    moles = reduce_list([molesC, molesH])
    moles = ["" if x == 1 else x for x in moles] #Remove all 1's
    return (f"C{moles[0]}H{moles[1]}")

class Calorimeter:
    def reaction_heat(self):
        raise NotImplementedError('Implemented in CoffeeCup and Bomb objects')

class CoffeeCup(Calorimeter, Reaction):
    def __init__(self, reactants, products):
        pass

    @staticmethod
    def reaction_heat(mass: float, spec_heat: float, d_temp: float):
        return mass * spec_heat * d_temp

class Bomb(Calorimeter, Combustion):
    def __init__(self, compound):
        Combustion.__init__(compound)

    @staticmethod
    def reaction_heat(spec_heat_calorimeter: float, d_temp: float):
        return spec_heat_calorimeter * d_temp
    