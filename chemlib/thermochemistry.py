from chemlib.chemistry import Combustion, Compound, Reaction
from chemlib.utils import reduce_list

# TODO: TEMP IMPLEMENTATIONS, NEED TO CONSIDER ADDITIONAL METHODS/CALCULATIONS
# INTERFACE?


def combustion_analysis(co2, h2o) -> str:
    carbon_moles = Compound("CO2").get_amounts(grams=co2)["moles"]
    hydrogen_moles = (Compound("H2O").get_amounts(grams=h2o)["moles"]) * 2
    moles = reduce_list([carbon_moles, hydrogen_moles])
    moles = ["" if x == 1 else x for x in moles]  # Remove all 1's
    return f"C{moles[0]}H{moles[1]}"


class Calorimeter:
    @staticmethod
    def reaction_heat(*args):
        raise NotImplementedError("Implemented in CoffeeCup and Bomb objects")


class CoffeeCup(Calorimeter, Reaction):
    @staticmethod
    def reaction_heat(mass: float, spec_heat: float, d_temp: float):
        return mass * spec_heat * d_temp


class Bomb(Calorimeter, Combustion):
    def __init__(self, compound):
        super().__init__(compound)

    @staticmethod
    def reaction_heat(spec_heat_calorimeter: float, d_temp: float):
        return spec_heat_calorimeter * d_temp
