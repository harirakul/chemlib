Chemical Compounds
========================================

Making a Compound
-----------------
.. autoclass:: chemlib.chemistry.Compound

Instantiate a ``chemlib.Compound`` object with a list of Element symbols.

.. code:: python

>>> from chemlib import Compound
>>> water = Compound(['H']*2 + ['O'])
>>> water.formula
'H₂O₁'

Molar Mass
----------
.. autofunction:: chemlib.chemistry.Compound.molar_mass

Get the molar mass (in g/mol) of the compound.

.. code:: python

>>> water.molar_mass()
18.01

Percentage Composition by Mass
------------------------------
.. autofunction:: chemlib.chemistry.Compound.percentage_by_mass

Get the percentage composition by mass of a certain element of the compound.

.. code:: python

>>> water.percentage_by_mass('H') #Percent of Hydrogen in Compound
11.183
>>> water.percentage_by_mass('O') #Percent of Oxygen in Compound
88.834

Stoichiometry
-------------
.. autofunction:: chemlib.chemistry.Compound.get_amounts

Accepting one argument. Use either ``grams=<float>``, ``moles=<float>``, or ``molecules=<float>``.
Returns a dictionary with corresponding mole, gram, and molecule values.

    >>> water.get_amounts(grams = 2)
    {'Compound': 'H₂O₁', 'Grams': 2, 'Moles': 0.111, 'Molecules': 6.685e+22}
    >>> water.get_amounts(moles = 2)
    {'Compound': 'H₂O₁', 'Grams': 36.02, 'Moles': 2, 'Molecules': 1.204e+24}
    >>> water.get_amounts(molecules = 2e+24)
    {'Compound': 'H₂O₁', 'Grams': 59.834, 'Moles': 3.3223, 'Molecules': 2e+24}