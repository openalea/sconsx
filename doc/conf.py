
###
#### read sphinx conf.py file
###from openalea.deploy.metainfo import compulsary_words, read_metainfo
###from openalea.misc.sphinx_configuration import *
###from openalea.misc.sphinx_tools import sphinx_check_version
###
###sphinx_check_version()                      # check that sphinx version is recent
###metadata = read_metainfo('../metainfo.ini') # read metainfo from common file with setup.py
###for key in compulsary_words:
###    exec("%s = '%s'" % (key, metadata[key]))
###
#### by product that need to be updated:
###latex_documents = [('contents', 'main.tex', project + ' documentation', authors, 'manual')]
###
###project = project + '.' + package
###
###
###
from __future__ import annotations

import importlib.metadata
import os
import sys

project = "sconsx"
copyright = "2025, OpenAlea"
author = "Christophe Pradal"
version = release = importlib.metadata.version("openalea.sconsx")


# Get the project root dir, which is the parent dir of this
cwd = os.getcwd()
project_root = os.path.dirname(cwd)

# Insert the project root dir as the first element in the PYTHONPATH.
# This lets us ensure that the source package is imported, and that its
# version is used.
sys.path.insert(0, os.path.join(project_root, 'src'))

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
]

source_suffix = [".rst", ".md"]
exclude_patterns = [
    "_build",
    "**.ipynb_checkpoints",
    "Thumbs.db",
    ".DS_Store",
    ".env",
    ".venv",
]

root_doc = 'contents'

autodoc_member_order = 'bysource'

html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "header_links_before_dropdown": 6,
    "sidebarwidth": 200,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/openalea/sconsx",
            "icon": "fa-brands fa-github",
        },
    ],
    "show_version_warning_banner": True,
    "footer_start": ["copyright"],
    "footer_center": ["sphinx-version"],
    "secondary_sidebar_items": {
        "**/*": ["page-toc", "edit-this-page", "sourcelink"],
        "examples/no-sidebar": [],
    },
    }

myst_enable_extensions = [
    "colon_fence",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

nitpick_ignore = [
    ("py:class", "_io.StringIO"),
    ("py:class", "_io.BytesIO"),
]

always_document_param_types = True
