# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Regression tests for standalone notebooks shared through molab and WASM."""

import ast
import subprocess
import sys
from pathlib import Path

import pytest

ASSETS = Path(__file__).resolve().parents[1] / "assets"
NOTEBOOKS = sorted(ASSETS.glob("**/notebooks/*.py"))
notebooks = pytest.mark.parametrize("notebook", NOTEBOOKS, ids=lambda path: str(path.relative_to(ASSETS)))



def is_setup_context(expression: ast.expr) -> bool:
    """Recognize setup blocks with or without display options."""
    context = expression.func if isinstance(expression, ast.Call) else expression
    return (
        isinstance(context, ast.Attribute)
        and isinstance(context.value, ast.Name)
        and (context.value.id == "app" and context.attr == "setup")
    )


@notebooks
def test_notebook_imports_use_setup(notebook: Path) -> None:
    """Keep notebook imports in setup, except for the marimo app bootstrap."""
    tree = ast.parse(notebook.read_text(encoding="utf-8"))
    setup_imports = {
        node
        for statement in tree.body
        if isinstance(statement, ast.With) and any(is_setup_context(item.context_expr) for item in statement.items)
        for node in ast.walk(statement)
        if isinstance(node, ast.Import | ast.ImportFrom)
    }
    bootstrap_imports = {
        node
        for node in tree.body
        if isinstance(node, ast.Import) and [(alias.name, alias.asname) for alias in node.names] == [("marimo", None)]
    }
    imports = {node for node in ast.walk(tree) if isinstance(node, ast.Import | ast.ImportFrom)}
    assert setup_imports, "Notebook must declare its imports in with app.setup"
    assert imports == setup_imports | bootstrap_imports, "Move notebook imports into with app.setup"


@notebooks
def test_notebook_without_workspace_packages(notebook: Path) -> None:
    """Run every notebook without access to locally installed workspace packages."""
    # Load installed dependencies without .pth files that expose editable workspace packages.
    code = (
        "import runpy, sys, sysconfig; "
        "sys.path.extend({sysconfig.get_path('purelib'), sysconfig.get_path('platlib')}); "
        "runpy.run_path(sys.argv[1])['app'].run()"
    )
    result = subprocess.run(
        [sys.executable, "-I", "-S", "-c", code, str(notebook)], capture_output=True, text=True, timeout=60, check=False
    )
    assert result.returncode == 0, result.stdout + result.stderr
