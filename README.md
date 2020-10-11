# chemlib

[![PyPI version](https://badge.fury.io/py/chemlib.svg)](https://badge.fury.io/py/chemlib) [![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/harirakul/chemlib/blob/master/LICENSE.txt) [![Documentation Status](https://readthedocs.org/projects/chemlib/badge/?version=latest)](https://chemlib.readthedocs.io/en/latest/?badge=latest)

Chemlib is a pure Python library that supports a variety of functions pertaining to the vast field of chemistry. It is under active development and continually improved to include more and more features.

Necessary data that provides properties of all the elements in the Periodic Table is found in [this csv file](https://github.com/harirakul/chemlib/blob/master/chemlib/resources/PTE_updated.csv).

## Installation
Use the Python Package Installer (PyPI):

```sh
$ pip install -U chemlib
```

## Features

- Properties of all Elements
- Compounds
   * Formula
   * Molar Mass
   * Percentage Composition by Mass
   * Stoichiometric Amounts
- Chemical Reactions
   * Formula
   * Balancing the Equation
   * Combustion Reactions
   * Stoichiometric Amounts
   * Limiting Reagent
- Quantum Mechanics
   * Electromagnetic Waves
      * Frequency, Wavelength, Energy per photon
   * Energy in nth Hydrogen Orbital

### Elements
```python
>>> from chemlib import Element

>>> boron = Element('B')   #Declare Element from its symbol

>>> boron.properties
{'AtomicNumber': 5.0, 'Element': 'Boron', 'Symbol': 'B', 'AtomicMass': 10.811, 'Neutrons': 6.0, 'Protons': 5.0, 'Electrons': 5.0, 'Period': 2.0, 'Group': 13.0, 'Phase': 'solid', 'Radioactive': False, 'Natural': True, 'Metal': False, 'Nonmetal': False, 'Metalloid': True, 'Type': 'Metalloid', 'AtomicRadius': '1.2', 'Electronegativity': 2.04, 'FirstIonization': '8.298', 'Density': '2.34', 'MeltingPoint': '2573.15', 'BoilingPoint': '4200', 'Isotopes': 6.0, 'Discoverer': 'Gay-Lussac', 'Year': '1808', 'SpecificHeat': '1.026', 'Shells': 2.0, 'Valence': 3.0, 'Config': '[He] 2s2 2p1', 'MassNumber': 11.0}

>>> boron.AtomicMass
10.811
```

### Compounds

```python
>>> from chemlib import Compound

>>> nitric_acid = Compound("HNO3")

>>> nitric_acid.occurences
{'H': 1, 'N': 1, 'O': 3}

>>> nitric_acid.molar_mass()
63.01

>>> nitric_acid.percentage_by_mass('O')  #Get percentage composition by mass of a constituent element of choice
76.174

```

### Stoichiometric conversions with compounds
Accepted inputs: grams, moles, and molecules

```python
>>> from chemlib import Compound

>>> water = Compound('H2O')

>>> water.formula
'H₂O₁'

>>> water.get_amounts(grams = 2)
{'Compound': 'H₂O₁', 'Grams': 2, 'Moles': 0.111, 'Molecules': 6.685e+22}

>>> water.get_amounts(moles = 1)
{'Compound': 'H₂O₁', 'Grams': 18.01, 'Moles': 1, 'Molecules': 6.02e+23}

>>> water.get_amounts(molecules = 1.0e+24)
{'Compound': 'H₂O₁', 'Grams': 29.917, 'Moles': 1.6611, 'Molecules': 1e+24}

```

### Balancing Chemical Reactions

```python

>>> from chemlib import Compound, Reaction

>>> H2 = Compound('H2')
>>> O2 = Compound('O2')
>>> H2O = Compound('H2O')
>>> r = Reaction(reactants = [H2, O2], products = [H2O])

>>> r.formula
'1H₂ + 1O₂ --> 1H₂O₁'

>>> r.is_balanced
False

>>> r.balance()

>>> r.formula
'2H₂ + 1O₂ --> 2H₂O₁'

>>> r.is_balanced
True
```

### To-Do

- [ ] Building Empirical Formulas
- [ ] Combustion Analysis
- [ ] Hydrates
- [ ] Percent Yield
- [ ] Molarity and pH
- [ ] Thermochemistry