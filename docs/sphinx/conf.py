# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Sphinx configuration for the CS00 API reference."""

# pylint: disable=invalid-name  # Sphinx requires lowercase configuration names.

project = "CS00 API"
author = "SGo-Go"
language = "en"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

autodoc_member_order = "bysource"
html_theme = "alabaster"
exclude_patterns = ["_build"]
