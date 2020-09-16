Core Data
========================================

Periodic Table
--------------
.. autoclass:: chemlib.chemistry.PeriodicTable

     >>> import chemlib
     >>> chemlib.PeriodicTable()
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

     Column Names

     >>> list(chemlib.pte)   #Column names
     ['AtomicNumber', 'Element', 'Symbol', 'AtomicMass', 'Neutrons', 'Protons', 'Electrons', 'Period', 'Group', 'Phase', 'Radioactive', 'Natural', 'Metal', 'Nonmetal', 'Metalloid', 'Type', 'AtomicRadius', 'Electronegativity', 'FirstIonization', 'Density', 'MeltingPoint', 'BoilingPoint', 'Isotopes', 'Discoverer', 'Year', 'SpecificHeat', 'Shells', 'Valence', 'Config', 'MassNumber']

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

{'AtomicNumber': 54.0, 'Element': 'Xenon', 
'Symbol': 'Xe', 'AtomicMass': 131.293, 'Neutrons': 77.0, 
'Protons': 54.0, 'Electrons': 54.0, 'Period': 5.0, 
'Group': 18.0, 'Phase': 'gas', 'Radioactive': False, 
'Natural': True, 'Metal': False, 'Nonmetal': True, 
'Metalloid': False, 'Type': 'Noble Gas', 
'AtomicRadius': '1.2', 'Electronegativity': nan, 
'FirstIonization': '12.1298', 'Density': '0.00589', 
'MeltingPoint': '161.45', 'BoilingPoint': '165.03', 
'Isotopes': 31.0, 'Discoverer': 'Ramsay and Travers', 
'Year': '1898', 'SpecificHeat': '0.158', 'Shells': 5.0, 
'Valence': 8.0, 'Config': '[Kr] 4d10 5s2 5p6', 
'MassNumber': 131.0}

    .. data:: chemlib.chemistry.Element.AtomicNumber
        :type: float
    .. data:: chemlib.chemistry.Element.Element
        :type: str
        :value: The name of the element
    .. data:: chemlib.chemistry.Element.Symbol
        :type: str
        :value: The symbol of the element
    .. data:: chemlib.chemistry.Element.AtomicMass
        :type: float
    .. data:: chemlib.chemistry.Element.Neutrons
        :type: float
    .. data:: chemlib.chemistry.Element.Protons
        :type: float
    .. data:: chemlib.chemistry.Element.Electrons
        :type: float
    .. data:: chemlib.chemistry.Element.Period
        :type: float
    .. data:: chemlib.chemistry.Element.Group
        :type: float
    .. data:: chemlib.chemistry.Element.Phase
        :type: str
        :value: The state of matter of the element at room temperature.
    .. data:: chemlib.chemistry.Element.Radioactive
        :type: boolean
    .. data:: chemlib.chemistry.Element.Natural
        :type: boolean
    .. data:: chemlib.chemistry.Element.Metal
        :type: boolean
    .. data:: chemlib.chemistry.Element.Nonmetal
        :type: boolean
    .. data:: chemlib.chemistry.Element.Metalloid
        :type: boolean
    .. data:: chemlib.chemistry.Element.Type
        :type: str
    .. data:: chemlib.chemistry.Element.AtomicRadius
        :type: str
    .. data:: chemlib.chemistry.Element.Electronegativity
        :type: str or NaN
    .. data:: chemlib.chemistry.Element.FirstIonization
        :type: str or NaN
    .. data:: chemlib.chemistry.Element.Density
        :type: float
    .. data:: chemlib.chemistry.Element.MeltingPoint
        :type: float
    .. data:: chemlib.chemistry.Element.BoilingPoint
        :type: float
    .. data:: chemlib.chemistry.Element.Isotopes
        :type: float
    .. data:: chemlib.chemistry.Element.Discoverer
        :type: str

Other Constants
---------------
Avogadro's Number

     >>> import chemlib
     >>> chemlib.AVOGADROS_NUMBER
     6.02e+23