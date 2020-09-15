Chemical Compounds
========================================

Making a Compound
-----------------

Instantiate a ``chemlib.Compound`` object with a list of Element symbols.

.. code:: python

>>> from chemlib import Compound
>>> water = Compound(['H']*2 + ['O'])

Molar Mass
----------

Get the molar mass (in g/mol) of the compound.

.. code:: python

>>> water.molar_mass()
18.01

Percentage Composition by Mass
------------------------------

Get the percentage composition by mass of a certain element of the compound.

.. code:: python

>>> water.percentage_by_mass('H')
11.183
>>> water.percentage_by_mass('O')
88.834