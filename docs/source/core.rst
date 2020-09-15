Core Data
========================================

Periodic Table
--------------

pandas Dataframe that contains the necessary background data.

.. code:: python

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

Columns of the Periodic Table (properties of each element)

.. code:: python
>>> list(chemlib.pte)   #Column names
['AtomicNumber', 'Element', 'Symbol', 'AtomicMass', 'Neutrons', 'Protons', 'Electrons', 'Period', 'Group', 'Phase', 'Radioactive', 'Natural', 'Metal', 'Nonmetal', 'Metalloid', 'Type', 'AtomicRadius', 'Electronegativity', 'FirstIonization', 'Density', 'MeltingPoint', 'BoilingPoint', 'Isotopes', 'Discoverer', 'Year', 'SpecificHeat', 'Shells', 'Valence', 'Config', 'MassNumber']

Other Constants
---------------

Avogadro's Number

.. code:: python

>>> import chemlib
>>> chemlib.AVOGADROS_NUMBER
6.02e+23