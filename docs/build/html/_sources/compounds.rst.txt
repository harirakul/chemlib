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

    .. data:: chemlib.chemistry.Compound.occurences
        :type: dict
    A dictionary containing the frequencies of the constituent elements in the compound.

    >>> water.occurences
    {'H': 2, 'O': 1}

Molar Mass
----------
.. autofunction:: chemlib.chemistry.Compound.molar_mass

Get the molar mass (in g/mol) of the compound.

.. code:: python

>>> water.molar_mass()
18.01

Percentage Composition by Mass
------------------------------
.. py:function:: chemlib.chemistry.Compound.percentage_by_mass(self, element)

   Get the percentage composition by mass of a certain element of the compound.

   :param str element: The constituent element of which the user wants to get percentage composition.
   :return: The percentage composition by mass of the element in the compound.
   :rtype: float

>>> water.percentage_by_mass('H') #Percent of Hydrogen in Compound
11.183
>>> water.percentage_by_mass('O') #Percent of Oxygen in Compound
88.834

Stoichiometry
-------------
.. py:function:: chemlib.chemistry.Compound.get_amounts(self, **kwargs)

   Get stoichiometric amounts of the compound given one measurement.

   :param int compound_number: The chosen compound in the reaction by order of appearance.
   :param kwargs: The amount of the chosen compound (grams=, moles=, or molecules=)
   :return: The gram, mole, and molecule amounts of the compound.
   :rtype: dict
   :raises ValueError: If the kwargs argument isn't either grams, moles, or molecules
   :raises ValueError: if more than one argument is given under kwargs

Get the amount of moles and molecules of water given 2 grams of water.

>>> water.get_amounts(grams = 2)
{'Compound': 'H₂O₁', 'Grams': 2, 'Moles': 0.111, 'Molecules': 6.685e+22}

Get the amount of grams and molecules of water given 2 moles of water.

>>> water.get_amounts(moles = 2)
{'Compound': 'H₂O₁', 'Grams': 36.02, 'Moles': 2, 'Molecules': 1.204e+24}

Get the amount of moles and grams of water given 2e+24 molecules of water.

>>> water.get_amounts(molecules = 2e+24)
{'Compound': 'H₂O₁', 'Grams': 59.834, 'Moles': 3.3223, 'Molecules': 2e+24}