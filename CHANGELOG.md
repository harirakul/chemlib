# chemlib Changelog

## v2.2.1 (5 June 2021)

- Holding off on image generation for Galvanic Cells (use `gcell.draw()` to manually generate diagram) - [Issue #11](https://github.com/harirakul/chemlib/issues/11)
- Fixed bug in the `limiting_reagent` method of the `chemlib.chemistry.Compound` class - [Issue #13](https://github.com/harirakul/chemlib/issues/13)

## v2.2.0 (15 May 2021)

- Added pH calculation
- Added equilibrium_concentrations method to Reactions
- Added `chemlib.utils.IceTable` and `chemlib.utils.Quantity`
- Fixed bugs in the `chemlib.quantum_mechanics.Wave` class

## v2.1.9 (17 January 2021)

- Removed the Periodic Table GUI (Made into a stand-alone application)
- Added classmethod ``by_formula`` to Reactions
- Added ``chemlib.utils.DimensionalAnalyzer`` to clean up code
- Fixed bugs in Compound initialization and accepting parentheses in formulae
- Added String overloading to Element, Compound, and Reaction
- Fixed bug in the Combustion class

## v2.1.8 (21 December 2020)

- Added Ptable GUI
- Fixed bug in Compound initialization

## v2.1.7 (17 December 2020)

- Added electrochemistry submodule