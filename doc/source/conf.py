# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import mlx.traceability
from pkg_resources import get_distribution
from pygments.formatters import LatexFormatter

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('../mlx'))

# -- Project information -----------------------------------------------------

project = 'mlx.xunit2rst'
copyright = '2019, Bavo Van Achte'
authors = ['Bavo Van Achte', 'Jasper Craeghs']

# The full version, including alpha/beta/rc tags
release = get_distribution('mlx.xunit2rst').version
version = '.'.join(release.split('.')[:2])

latex_documents = [
    ('index', 'xunit2rst.tex', 'Script to convert .robot files to .rst files with traceable items',
     ' \\and '.join(authors), 'manual', True),
]

man_pages = [
    ('index', 'xunit2rst', 'Script to convert .robot files to .rst files with traceable items',
     authors, 1)
]

# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ('index', 'xunit2rst', 'xunit2rst conversion script', '@*'.join(authors), 'xunit2rst',
     'Script to convert .robot files to .rst files with traceable items.', 'Miscellaneous'),
]

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinxcontrib_robotdoc',
    'mlx.traceability',
]

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    'preamble': r'\usepackage{fancyvrb}'
                r'\usepackage{color}'
                + LatexFormatter().get_style_defs(),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Additional attributes for traceability plugin
traceability_relationships = {
    'passes': 'passed_by',
    'fails': 'failed_by',
    'validates': 'validated_by',
}
traceability_relationship_to_string = {
    'passes': 'Passes',
    'passed_by': 'Passed by',
    'fails': 'Fails',
    'failed_by': 'Failed by',
    'validates': 'Validates',
    'validated_by': 'Validated by',
}
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = [os.path.join(os.path.dirname(mlx.traceability.__file__), 'assets')]

traceability_render_relationship_per_item = True

def setup(app):
    pass
