# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
# pylint: disable=import-outside-toplevel
#
# faucet documentation build configuration file, created by
# sphinx-quickstart on Thu Oct 26 13:48:25 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

'''
Faucet's Sphinx configuration
'''

import os
import sys

sys.path.insert(0, os.path.abspath('../'))

autodoc_default_options = {
    'members': True,
    'show-inheritance': True,
    'undoc-members': True,
}

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
needs_sphinx = '1.8'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.coverage',
              'sphinx.ext.doctest',
              'sphinx.ext.githubpages',
              'sphinx.ext.napoleon',
              'sphinx.ext.viewcode',
              'sphinxcontrib.rsvgconverter'
              ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
copyright = '2018-2021, Faucet Developers'  # pylint: disable=redefined-builtin
author = 'Faucet Developers'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'README.rst', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
    ]
}


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'faucetdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'faucet.tex', 'Faucet Documentation',
     'Faucet Developers', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'faucet', 'Faucet Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'faucet', 'Faucet Documentation',
     author, 'faucet', '',
     'Miscellaneous'),
]

# -- Magic to run sphinx-apidoc automatically -----------------------------

# See https://github.com/rtfd/readthedocs.org/issues/1139
# on which this is based.


def run_apidoc(_):
    """Call sphinx-apidoc on faucet module"""

    from sphinx.ext.apidoc import main as apidoc_main
    apidoc_main(['-e', '-o', 'source/apidoc', '../faucet'])


def generate_prometheus_metric_table(_):
    """Autogen prometheus metrics documentation"""

    import faucet.faucet_metrics
    import faucet.gauge_prom
    from prometheus_client import CollectorRegistry

    block_text = {}
    output_path = {
        'faucet': 'autogen/faucet_prometheus_metric_table.rst',
        'gauge': 'autogen/gauge_prometheus_metric_table.rst'
    }

    metrics = {
        'faucet': faucet.faucet_metrics.FaucetMetrics(reg=CollectorRegistry()),
        'gauge': faucet.gauge_prom.GaugePrometheusClient(reg=CollectorRegistry())
    }

    for module in ["faucet", "gauge"]:
        block_text[module] = """\
.. list-table:: {} prometheus metrics
    :widths: 40 10 55
    :header-rows: 1

    * - Metric
      - Type
      - Description
""".format(module.title())

        # pylint: disable=protected-access
        for metric in metrics[module]._reg.collect():
            if metric.type == "counter":
                metric_name = "{}_total".format(metric.name)
            else:
                metric_name = metric.name

            block_text[module] += """\
    * - {}
      - {}
      - {}
""".format(metric_name, metric.type, metric.documentation)

        with open(output_path[module], 'w', encoding='utf-8') as output_file:
            output_file.write(block_text[module])


def setup(app):
    """ Add hooks into Sphinx to change behaviour and autogen documentation """

    # Add custom css
    app.add_css_file("css/responsive-tables.css")
    # Override Sphinx setup to trigger sphinx-apidoc.
    app.connect('builder-inited', run_apidoc)
    app.connect('builder-inited', generate_prometheus_metric_table)
