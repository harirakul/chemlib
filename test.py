import pandas as pd
import numpy as np
import sympy
from fractions import Fraction
import re
import os

from chemlib.utils import DimensionalAnalyzer 
from chemlib.parse import parse_formula
from chemlib.constants import Kw, AVOGADROS_NUMBER
import chemlib.chemistry as chem

P = 43.64
O = 100 - P
empirical = chem.empirical_formula_by_percent_comp(P = P, O = O)
print(empirical)
