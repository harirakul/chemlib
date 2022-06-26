from chemlib.chemistry import PeriodicTable
from chemlib.chemistry import Element, Compound, Reaction, Combustion, Solution
from chemlib.chemistry import empirical_formula_by_percent_comp, pH

from chemlib.quantum_mechanics import Wave, rydberg
from chemlib.quantum_mechanics import energy_of_hydrogen_orbital

from chemlib.electrochemistry import electrolysis, F, GalvanicCell

from chemlib.thermochemistry import combustion_analysis

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
AVOGADROS_NUMBER = 6.02e23
