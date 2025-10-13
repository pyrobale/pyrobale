import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# -- Extensions ------------------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.githubpages',
    'autoapi.extension',
    'sphinx_copybutton',
    'sphinx_design',
]
# -- AutoAPI configuration -------------------------------------------------
autoapi_dirs = ['../../pyrobale']
autoapi_type = 'python'
autoapi_root = 'api'
autoapi_options = [
    'members',
    'undoc-members',
    'show-inheritance',
    'show-module-summary',
    'special-members',
]

autoapi_add_toctree_entry = True
autoapi_keep_files = False

# -- Napoleon settings -----------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

# -- General configuration -------------------------------------------------
project = 'Pyrobale'
copyright = '2025, Ali Safamanesh & Aydin Rahbaran'
author = 'Ali Safamanesh & Aydin Rahbaran'

# -- HTML output -----------------------------------------------------------
html_theme = 'furo'
html_theme = 'furo'
html_title = 'Pyrobale Documentation'

html_theme_options = {
    "top_of_page_button": "arrow",
    "source_repository": "https://github.com/pyrobale/pyrobale",
    "source_branch": "main",
    "source_directory": "docs/source/",
    "navigation_with_keys": True,
    "announcement": "<strong>🚀 Pyrobale Beta!</strong> - Modern library for Bale bot API",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/yourusername/pyrobale",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}

html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
        "sidebar/ethical-ads.html",
        "sidebar/extra-navigation.html",
        "sidebar/project-links.html",
        "sidebar/scroll-end.html",
    ]
}

html_static_path = ['_static']
html_show_sourcelink = False
html_css_files = [
    'css/custom.css',
]

# -- Logo --------------------------------------------------------------------
html_logo = '../../pyrobale.png'
html_favicon = '../../pyrobale.png'

# -- Autodoc configuration -------------------------------------------------
autodoc_typehints = 'description'
autodoc_member_order = 'bysource'

exclude_patterns = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'