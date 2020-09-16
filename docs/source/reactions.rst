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
        :type: bool

    >>> r.is_balanced
    False

Balancing the Equation
----------------------
.. autofunction:: chemlib.chemistry.Reaction.balance

Balances the chemical equation using linear algebra. See `Applications of Linear Algebra in Chemistry <http://www.math.utah.edu/~gustafso/s2017/2270/projects-2016/sanchezDario-chemistry-balancing-chemical-equations.pdf>`_. 

    >>> r.balance()
    >>> r.formula
    '1N₂O₅ + 1H₂O₁ --> 2H₁N₁O₃'
    >>> r.is_balanced
    True