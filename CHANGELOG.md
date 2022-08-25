# chemlib Changelog

## v2.2.4 (25 August 2022)

- Fixed major bug with limited amount of reactants/products in Balancing Reactions - [Issue #45](https://github.com/harirakul/chemlib/pull/45)
- Fixed bug with Empirical Formula generation - [Issue #41](https://github.com/harirakul/chemlib/issues/41)
- Removed rounding altogether to avoid inaccurate calculations - [Issue #34](https://github.com/harirakul/chemlib/issues/34)
- Cleaned data types and null values from Periodic Table CSV - [PR #44](https://github.com/harirakul/chemlib/pull/44)
- Added reduction potentials for halogenes F, Cl, Br and I - [PR #23](https://github.com/harirakul/chemlib/pull/23)
- Overloaded the `==` operator for the `Compound` class, allowing for easy checking of equality between compounds

## v2.2.3 (13 February 2022)

- Fixed bug with initialization of Ds, Rg, and Cn - [Issue #27](https://github.com/harirakul/chemlib/issues/27)
- Added classmethod ``by_num`` to the Element class

## v2.2.2 (2 November 2021)

- Fixed major bug with H6C6 combustion in Balancing Equations - [Issue #19](https://github.com/harirakul/chemlib/issues/19)

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