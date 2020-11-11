Aqueous Solutions
========================================

Making a Solution
-----------------
.. py:class:: chemlib.chemistry.Solution(self, solute, molarity)
Instantiate a ``chemlib.Solution`` object with the formula of the solute, and the molarity in mol/L.

   :param solute (str): The formula of the solute without using subscripts OR a ``chemlib.chemistry.Compound`` object.
   :param molarity (float): How many moles of solute per liter of solution

>>> from chemlib import Solution
>>> Solution('AgCl', 2)
<chemlib.chemistry.Solution object at 0x03F46370>
>>> s = Solution('AgCl', 2)
>>> s.molarity
2

.. py:classmethod:: chemlib.chemistry.Solution.by_grams_per_liters(cls, solute, grams, liters)
OR you can make a Solution with the solute, and grams per liter.

   :param str solute: The formula of the solute without using subscripts OR a ``chemlib.chemistry.Compound`` object.
   :param float grams: How many grams of solute
   :param float liters: How many liters of solution

>>> from chemlib import Solution
>>> s = Solution.by_grams_per_liters("NaCl", 10, 1)
>>> s.molarity
0.1711

Dilutions
---------
.. py:function:: chemlib.chemistry.Solution.dilute(self, V1 = None, M2 = None, V2 = None, inplace = False) -> dict
Using formula M1*V1 = M2*V2

   :param float V1: The starting volume of the solution. [Must be specified]
   :param float M2: The ending molarity after dilution.
   :param float V2: The ending volume after dilution
   :param bool inplace: You can set to true if the old molarity is to be replaced by the new molarity
   :return: The new volume and the new molarity.
   :rtype: dict
   :raises TypeError: if a starting volume is not specified
   :raises TypeError: if both M2 and V2 are specified

To find the dilution of 2.5 L of 0.25M NaCl to a 0.125M NaCl solution:

>>> from chemlib import Solution
>>> s = Solution("NaCl", 0.25)
>>> s.dilute(V1 = 2.5, M2 = 0.125)
{'Solute': 'Na₁Cl₁', 'Molarity': 0.125, 'Volume': 5.0}