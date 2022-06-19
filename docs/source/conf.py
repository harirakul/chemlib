# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import sphinx_rtd_theme
from recommonmark.parser import CommonMarkParser
import typing

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

_get_type_hints = typing.get_type_hints


def get_type_hints(obj, globalns=None, localns=None):
    if localns is None:
        localns = {}
    return _get_type_hints(obj, globalns, localns)


typing.get_type_hints = get_type_hints

autodoc_mock_imports = [
    "chemlib",
    "numpy",
    "sympy",
    "pandas",
    "typing",
    "sphinx",
    "Pillow",
    "sphinx_rtd_theme",
]

# -- Project information -----------------------------------------------------

project = "chemlib"
copyright = "2020, Hari Ambethkar"
author = "Hari Ambethkar"

# The full version, including alpha/beta/rc tags
release = "v1.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "recommonmark",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
]

autodoc_member_order = "bysource"
source_suffix = [".rst", ".md"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
# html_logo = "chememelogo2.png"
pygments_style = "sphinx"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
master_doc = "index"
