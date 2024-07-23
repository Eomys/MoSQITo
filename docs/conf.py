# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html



# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MOSQITO'
copyright = '2024, Green Forge Coop'
author = 'Green Forge Coop'
version = "1.2.1"
release = version

import os
import sys
sys.path.insert(0, os.path.abspath(".."))

# Remove rst files of the folder having the name than some functions
if os.path.isfile('source/reference/mosqito.sq_metrics.loudness.loudness_zwst.rst'):
    os.remove('source/reference/mosqito.sq_metrics.loudness.loudness_zwst.rst')
    os.remove('source/reference/mosqito.sq_metrics.loudness.loudness_zwtv.rst')
    os.remove('source/reference/mosqito.sq_metrics.roughness.roughness_dw.rst')
    os.remove('source/reference/mosqito.sq_metrics.roughness.roughness_ecma.rst')

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'matplotlib.sphinxext.plot_directive',
    'matplotlib.sphinxext.mathmpl',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinxcontrib.bibtex'
]

templates_path = ['templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
bibtex_bibfiles = ['ref.bib']
bibtex_default_style = 'plain'
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_favicon = 'source/_static/favicon.ico'
html_theme = 'pydata_sphinx_theme'
html_title = "MOSQITO manual"
html_last_updated_fmt = '%b %d, %Y'
html_context = {"default_mode": "light"}
html_use_modindex = True
html_copy_source = False
html_domain_indices = False
html_file_suffix = '.html'
htmlhelp_basename = 'mosqito'
html_css_files = ['source/_static/custom.css',
]

html_theme_options = {
  "logo": {
      "text": "MOSQITO",
      "image_light": 'source/_static/logo.png',
      "image_dark": 'source/_static/logo.png',
  },
  "github_url": "https://github.com/Eomys/MoSQITo",
  "collapse_navigation": True,
  "show_prev_next": False,
  "show_nav_level": 0,
  "navigation_depth": 3,
}

autosummary_generate = True
add_module_names = False

autodoc_default_options = {
    'members': True,
    # The ones below should be optional but work nicely together with
    # example_package/autodoctest/doc/source/_templates/autosummary/class.rst
    # and other defaults in sphinx-autodoc.
    'show-inheritance': True,
    'inherited-members': True,
    'no-special-members': True,
}

# Monkey-patch autosummary template context
from sphinx.ext.autosummary.generate import AutosummaryRenderer


def smart_fullname(fullname):
    parts = fullname.split(".")
    return ".".join(parts[1:])


def fixed_init(self, app, template_dir=None):
    AutosummaryRenderer.__old_init__(self, app, template_dir)
    self.env.filters["smart_fullname"] = smart_fullname


AutosummaryRenderer.__old_init__ = AutosummaryRenderer.__init__
AutosummaryRenderer.__init__ = fixed_init

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.environment.collectors.title import TitleCollector

_process_doc = TitleCollector.process_doc

def process_doc(self, app: Sphinx, doctree: nodes.document) -> None:
    if doctree.traverse(nodes.section):
        _process_doc(self, app, doctree)
    else:
        titlenode = nodes.title()
        app.env.titles[app.env.docname] = titlenode
        app.env.longtitles[app.env.docname] = titlenode

TitleCollectorprocess_doc = process_doc

def crawl_source_shorten_titles(path):

    # List files in directory
    for file_name in os.listdir(path):

        # Build path to file
        file_path = os.path.join(path, file_name)

        # Modify .rst source file title
        _, extension = os.path.splitext(file_path)
        if extension == ".rst":
            with open(file_path, 'r') as file:
                lines = file.readlines()
            if lines[0]=='\n':
                idx = file_name[:-4].rfind(".")
                name = file_name[idx+1:-4]
                # modify title, write back to file                
                lines[0] = name + '\n'
                lines[1] = "=======================================================\n"
                with open(file_path, 'w') as file:
                    file.writelines(lines)

# Remove parents from titles in all .rst files
crawl_source_shorten_titles(os.path.abspath("") + "/source/reference")

