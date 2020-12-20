Core Data
========================================

Periodic Table
--------------
.. autoclass:: chemlib.chemistry.PeriodicTable
    :members:
    :show-inheritance:

Column Names

>>> list(chemlib.pte)   #Column names
['AtomicNumber', 'Element', 'Symbol', 'AtomicMass', 'Neutrons', 'Protons', 'Electrons', 'Period', 'Group', 'Phase', 'Radioactive', 'Natural', 'Metal', 'Nonmetal', 'Metalloid', 'Type', 'AtomicRadius', 'Electronegativity', 'FirstIonization', 'Density', 'MeltingPoint', 'BoilingPoint', 'Isotopes', 'Discoverer', 'Year', 'SpecificHeat', 'Shells', 'Valence', 'Config', 'MassNumber']

PTable GUI
----------
>>> import chemlib
>>> chemlib.GUI()

.. image:: ../../chemlib/screenshots/PTable.png
    :alt: PTable

Elements
--------
.. autoclass:: chemlib.chemistry.Element

Contains all the properties of the respective element:

.. code:: python
>>> from chemlib import Element
>>> xenon = Element('Xe') #Instantiate with symbol of Element
>>> xenon.properties
{'AtomicNumber': 54.0, 'Element': 'Xenon', 'Symbol': 'Xe', 'AtomicMass': 131.293, 'Neutrons': 77.0, 'Protons': 54.0, 'Electrons': 54.0, 'Period': 5.0, 'Group': 18.0, 'Phase': 'gas', 'Radioactive': False, 'Natural': True, 'Metal': False, 'Nonmetal': True, 'Metalloid': False, 'Type': 'Noble Gas', 'AtomicRadius': '1.2', 'Electronegativity': nan, 'FirstIonization': '12.1298', 'Density': '0.00589', 'MeltingPoint': '161.45', 'BoilingPoint': '165.03', 'Isotopes': 31.0, 'Discoverer': 'Ramsay and Travers', 'Year': '1898', 'SpecificHeat': '0.158', 'Shells': 5.0, 'Valence': 8.0, 'Config': '[Kr] 4d10 5s2 5p6', 'MassNumber': 131.0}
>>> xenon.AtomicMass
131.293
>>> xenon.FirstIonization
'12.1298'

    .. py:data:: chemlib.chemistry.Element.AtomicNumber
        :type: float
    .. py:data:: chemlib.chemistry.Element.Element
        :type: str
        :value: The name of the element
    .. py:data:: chemlib.chemistry.Element.Symbol
        :type: str
        :value: The symbol of the element
    .. py:data:: chemlib.chemistry.Element.AtomicMass
        :type: float
    .. py:data:: chemlib.chemistry.Element.Neutrons
        :type: float
    .. py:data:: chemlib.chemistry.Element.Protons
        :type: float
    .. py:data:: chemlib.chemistry.Element.Electrons
        :type: float
    .. py:data:: chemlib.chemistry.Element.Period
        :type: float
    .. py:data:: chemlib.chemistry.Element.Group
        :type: float
    .. py:data:: chemlib.chemistry.Element.Phase
        :type: str
        :value: The state of matter of the element at room temperature.
    .. py:data:: chemlib.chemistry.Element.Radioactive
        :type: boolean
    .. py:data:: chemlib.chemistry.Element.Natural
        :type: boolean
    .. py:data:: chemlib.chemistry.Element.Metal
        :type: boolean
    .. py:data:: chemlib.chemistry.Element.Nonmetal
        :type: boolean
    .. py:data:: chemlib.chemistry.Element.Metalloid
        :type: boolean
    .. py:data:: chemlib.chemistry.Element.Type
        :type: str
    .. py:data:: chemlib.chemistry.Element.AtomicRadius
        :type: str
    .. py:data:: chemlib.chemistry.Element.Electronegativity
        :type: str or NaN
    .. py:data:: chemlib.chemistry.Element.FirstIonization
        :type: str or NaN
    .. py:data:: chemlib.chemistry.Element.Density
        :type: float
    .. py:data:: chemlib.chemistry.Element.MeltingPoint
        :type: float
    .. py:data:: chemlib.chemistry.Element.BoilingPoint
        :type: float
    .. py:data:: chemlib.chemistry.Element.Isotopes
        :type: float
    .. py:data:: chemlib.chemistry.Element.Discoverer
        :type: str

Other Constants
---------------
.. py:data:: chemlib.AVOGADROS_NUMBER
    :type: float
    :value: 6.02e+23

    Contains Avogaadro's Number, which  relates the number of constituent particles in a sample with the amount of substance in that sample.

     >>> import chemlib
     >>> chemlib.AVOGADROS_NUMBER
     6.02e+23

.. py:data:: chemlib.c
    :type: float
    :value: 2.998e+8

The speed of light.

.. py:data:: chemlib.h
    :type: float
    :value: 6.626e-34

Planck's constant.

.. py:data:: chemlib.R
    :type: float
    :value: 1.0974e+7

Rydberg constant.