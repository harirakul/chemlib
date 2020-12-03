Empirical Formulae
========================================

EF by Percentage Composition
----------------------------
.. py:function:: chemlib.chemistry.empirical_formula_by_percent_comp(**kwargs)

    Get the empirical formula given the percentage compositions of all elements in the compound.

   :param kwargs: The percentage compositions of elements in the compound ``(<Element symbol> = <Percentage Composition> ...)``
   :return: The empirical formula of the compound.
   :rtype: str
   :raises ValueError: If the sums of the percentages is not equal to 100.

Get the empirical formula of a compound that is composed of 80.6% C, and 19.4% H by mass:

>>> from chemlib import empirical_formula_by_percent_comp as efbpc
>>> efbpc(C = 80.6, H = 19.4)
'C1H3'

Combustion Analysis
-------------------
.. py:function:: chemlib.chemistry.combustion_analysis(CO2, H2O)

    Get the empirical formula of a hydrocarbon given the grams of CO2 and grams of H2O formed from its combustion.

   :param CO2: The grams of carbon dioxide formed as a result of the combustion of the hydrocarbon.
   :param H2O: The grams of water formed as a result of the combustion of the hydrocarbon.
   :return: The empirical formula of the hydrocarbon.
   :rtype: str

A hydrocarbon fuel is fully combusted with 18.214 g of oxygen to yield 23.118 g of carbon
dioxide and 4.729 g of water. Find the empirical formula for the hydrocarbon.

>>> from chemlib.chemistry import combustion_analysis
>>> combustion_analysis(23.118, 4.729)
'CH'