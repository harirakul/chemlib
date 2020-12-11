Electrochemistry
========================================

Electrolysis
------------
.. py:function:: chemlib.electrochemistry.electrolysis(element: str, n: int, **kwargs) -> dict:

   :param element (str): The symbol of a chemical element.
   :param n (int): The moles of electrons transferred.
   :param kwargs: Provide two of the values from amps, seconds, and grams.
   :raises TypeError: If not only 2 of the parameters in kwargs are specified.

`Example:`
Copper metal is purified by electrolysis. How much copper metal (in grams) could be produced from copper (ii) oxide by applying a current of 10.0 amps at the appropriate negative potential for 12.0 hours?

>>> from chemlib import electrolysis
>>> electrolysis('Cu', 2, amps = 10, seconds=12*60*60)
{'element': 'Cu', 'n': 2, 'seconds': 43200, 'amps': 10, 'grams': 142.25979167746283}
>>> 
