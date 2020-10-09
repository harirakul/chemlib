Quantum Mechanics
========================================

Electromagnetic Waves
---------------------
.. py:class:: chemlib.quantum_mechanics.Wave(**kwargs)
Makes a Wave object given either wavelength (in meters), frequency (in Hz), or energy (in J per photon), and calculates the aforementioned values.

:param kwargs: The value of the known variable (wavelength=, frequency=, or energy=)

Determine the wavelength, frequency, and energy of a wave with frequency 2e+17 Hz:

>>> from chemlib import Wave
>>> w = Wave(frequency=2e+17)
>>> w.properties
{'wavelength': 1.499e-09, 'frequency': 2e+17, 'energy': 1.325e-16}

Determine the wavelength, frequency, and energy of a wave with wavelength 3e-9 m:

>>> w = Wave(wavelength=3e-9)
>>> w.properties
{'wavelength': 3e-09, 'frequency': 9.993e+16, 'energy': 6.622e-17}

Determine the wavelength, frequency, and energy of a wave with energy 3e-15 Joules per particle:

>>> from chemlib import Wave
>>> w = Wave(energy=3e-15)
>>> w.properties
{'wavelength': 4.387e-44, 'frequency': 4.528e+18, 'energy': 3e-15}