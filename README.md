# chemlib: a pure Python chemistry library

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/harirakul/chemlib/blob/master/LICENSE.txt)

An easy-to-use library that quickly performs chemistry calculations.

## Installation
```
pip install chemlib
```

## Features

Periodic table as a ```pandas.Dataframe``` object

```python
>>> import chemlib

>>> chemlib.pte
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
```

```chemlib.Element``` class with easily accessible properties

```python
>>> from chemlib import Element

>>> boron = Element('B')   #Declare Element from its symbol

>>> boron.properties
{'AtomicNumber': 5.0, 'Element': 'Boron', 'Symbol': 'B', 'AtomicMass': 10.811, 'Neutrons': 6.0, 'Protons': 5.0, 'Electrons': 5.0, 'Period': 2.0, 'Group': 13.0, 'Phase': 'solid', 'Radioactive': False, 'Natural': True, 'Metal': False, 'Nonmetal': False, 'Metalloid': True, 'Type': 'Metalloid', 'AtomicRadius': '1.2', 'Electronegativity': 2.04, 'FirstIonization': '8.298', 'Density': '2.34', 'MeltingPoint': '2573.15', 'BoilingPoint': '4200', 'Isotopes': 6.0, 'Discoverer': 'Gay-Lussac', 'Year': '1808', 'SpecificHeat': '1.026', 'Shells': 2.0, 'Valence': 3.0, 'Config': '[He] 2s2 2p1', 'MassNumber': 11.0}

>>> boron.AtomicMass
10.811
```

```chemlib.Compound``` 

```python
>>> from chemlib import Compound

>>> nitric_acid = Compound(['H', 'N'] + ['O']*3)

>>> nitric_acid.occurences
{'H': 1, 'N': 1, 'O': 3}

>>> nitric_acid.molar_mass()
63.01

>>> nitric_acid.percentage_by_mass('O')  #Get percentage composition by mass of a constituent element of choice
76.174

```

Stoichiometric conversions with compounds (accepted inputs: grams, moles, and molecules)

```python
>>> from chemlib import Compound

>>> water = Compound(['H'] + ['O']*2)

>>> water.get_amounts(grams = 2)
{'Compound': 'H₁O₂', 'Grams': 2, 'Moles': 0.0606, 'Molecules': 3.647e+22}

>>> water.get_amounts(moles = 1)
{'Compound': 'H₁O₂', 'Grams': 33.01, 'Moles': 1, 'Molecules': 6.02e+23}

>>> water.get_amounts(molecules = 1.0e+24)
{'Compound': 'H₁O₂', 'Grams': 54.834, 'Moles': 1.6611, 'Molecules': 1e+24}


```

