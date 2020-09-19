Chemical Reactions
========================================

Making a Reaction
-----------------
.. autoclass:: chemlib.chemistry.Reaction

Instantiate a ``chemlib.Reaction`` object with a list of reactant Compounds and product Compounds.

>>> from chemlib import Compound, Reaction
>>> N2O5 = Compound(['N']*2 + ['O']*5)
>>> H2O = Compound(['H']*2 + ['O'])
>>> HNO3 = Compound(['H', 'N'] + ['O']*3)
>>> r = Reaction([N2O5, H2O], [HNO3])

    .. data:: chemlib.chemistry.Reaction.formula
        :type: str

    >>> r.formula
    '1N₂O₅ + 1H₂O₁ --> 1H₁N₁O₃'

    .. data:: chemlib.chemistry.Reaction.is_balanced
        :type: boolean

    >>> r.is_balanced
    False

    .. data:: chemlib.chemistry.Reaction.reactant_formulas
        :type: list
    
    >>> r.reactant_formulas
    ['N₂O₅', 'H₂O₁']

    .. data:: chemlib.chemistry.Reaction.product_formulas
        :type: list
    
    >>> r.product_formulas
    ['H₁N₁O₃']

Combustion Reactions
--------------------
.. py:class:: chemlib.chemistry.Combustion(compound)
Inherits from ``chemlib.chemistry.Reaction``

Makes a chemical reaction involving the combustion of one compound. Formula will be balanced.

>>> from chemlib import Compound, Combustion
>>> methane = Compound(['C'] + ['H']*4)
>>> c = Combustion(methane)
>>> c.formula
'1C₁H₄ + 2O₂ --> 2H₂O₁ + 1C₁O₂'
>>> c.is_balanced
True

Balancing the Equation
----------------------
.. py:function:: chemlib.chemistry.Reaction.balance(self) -> None

Balances the chemical equation using linear algebra. See `Applications of Linear Algebra in Chemistry <http://www.math.utah.edu/~gustafso/s2017/2270/projects-2016/sanchezDario-chemistry-balancing-chemical-equations.pdf>`_. 

    >>> r.balance()
    >>> r.formula
    '1N₂O₅ + 1H₂O₁ --> 2H₁N₁O₃'
    >>> r.is_balanced
    True

Stoichiometry
-------------

.. py:function:: chemlib.chemistry.Reaction.get_amounts(self, compound_number, **kwargs)

   Get stoichiometric amounts of ALL compounds in the reaction given the amount of one compound.

   :param int compound_number: The chosen compound in the reaction by order of appearance.
   :param kwargs: The amount of the chosen compound (grams=, moles=, or molecules=)
   :return: the amounts of each compound in the reaction
   :rtype: list of dicts
   :raises ValueError: if the compound_number is less than 1 or greater than the number of compounds in the reaction
   :raises ValueError: if more than one argument is given under kwargs

Best demonstrated by example:

>>> r.formula
'1N₂O₅ + 1H₂O₁ --> 2H₁N₁O₃'

Get the amounts of ALL compounds in the above reaction given 5 grams of N₂O₅. It is the first compound in the reaction by order of appearance (left to right).

>>> r.get_amounts(1, grams=5)
[{'Compound': 'N₂O₅', 'Grams': 5, 'Moles': 0.0463, 'Molecules': 2.787e+22}, {'Compound': 'H₂O₁', 'Grams': 0.834, 'Moles': 0.0463, 'Molecules': 2.787e+22}, {'Compound': 'H₁N₁O₃', 'Grams': 5.835, 'Moles': 0.0926, 'Molecules': 5.575e+22}]

Get the amounts of ALL compounds in the above reaction given 3.5 moles of HNO₃. It is the third compound in the reaction by order of appearance (left to right).

>>> r.get_amounts(3, moles=3.5)
[{'Compound': 'N₂O₅', 'Grams': 189.018, 'Moles': 1.75, 'Molecules': 1.054e+24}, {'Compound': 'H₂O₁', 'Grams': 31.518, 'Moles': 1.75, 'Molecules': 1.054e+24}, {'Compound': 'H₁N₁O₃', 'Grams': 220.535, 'Moles': 3.5, 'Molecules': 2.107e+24}]

Limiting Reagent
----------------
.. py:function:: chemlib.chemistry.Reaction.limiting_reagent(self, *args, mode = 'grams')

   Get the limiting reagent (limiting reactant) in the chemical reaction.

   :param args: The amounts of each reactant to use in the chemical reaction. 
   :param str mode: The units of each amount in args. Default is grams, can also be moles or molecules.
   :return: The limiting reagent of the reaction.
   :rtype: chemlib.chemistry.Compound
   :raises TypeError: If the number of args doesn't match the number of reactants in the reaction.
   :raises ValueError: If the mode is not grams, moles, or molecules.

   Find the limiting reagent of the reaction when using 50 grams of the first reactant (N₂O₅) and 80 grams of the second reactant (H₂O):

    >>> lr = r.limiting_reagent(50, 50)
    >>> lr.formula
    'N₂O₅'

   Find the limiting reagent of the reaction when using 3 moles of the first reactant (N₂O₅) and 1 mole of the second reactant (H₂O):

    >>> lr = r.limiting_reagent(3, 1, mode = 'moles')
    >>> lr.formula
    'H₂O₁'