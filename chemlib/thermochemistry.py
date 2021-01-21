from chemlib.chemistry import Combustion, Reaction

# TODO: TEMP IMPLEMENTATIONS, NEED TO CONSIDER ADDITIONAL METHODS/CALCULATIONS  
# INTERFACE?
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
    