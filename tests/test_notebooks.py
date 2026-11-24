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


def app_decorator_name(decorator: ast.expr) -> str | None:
    """Return a Marimo app decorator's name when present."""
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "app":
        return target.attr
    return None


def has_hide_code(decorator: ast.expr) -> bool:
    """Return whether a Marimo decorator explicitly hides its source."""
    return isinstance(decorator, ast.Call) and any(
        keyword.arg == "hide_code" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True
        for keyword in decorator.keywords
    )


def is_standalone_markdown_cell(cell: ast.FunctionDef) -> bool:
    """Recognize a cell whose only output is one direct mo.md call."""
    statements = [statement for statement in cell.body if not isinstance(statement, ast.Return)]
    if len(statements) != 1 or not isinstance(statements[0], ast.Expr):
        return False
    expression = statements[0].value
    return (
        isinstance(expression, ast.Call)
        and isinstance(expression.func, ast.Attribute)
        and isinstance(expression.func.value, ast.Name)
        and expression.func.value.id == "mo"
        and expression.func.attr == "md"
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


@pytest.mark.parametrize(
    "notebook_name",
    (
        "binary_counter.py",
        "hex_viewer.py",
        "image_viewer.py",
        "huffman_coding.py",
        "caesar_cipher.py",
        "modular_multiplication.py",
    ),
)
def test_selected_playgrounds_hide_all_sources(notebook_name: str) -> None:
    """Hide setup, cell, and function source in the five selected playgrounds."""
    notebook = ASSETS / "lecture01" / "notebooks" / notebook_name
    tree = ast.parse(notebook.read_text(encoding="utf-8"))

    setup_blocks = [
        node
        for node in tree.body
        if isinstance(node, ast.With) and any(is_setup_context(item.context_expr) for item in node.items)
    ]
    assert setup_blocks, f"{notebook_name} must define app.setup"
    for setup_block in setup_blocks:
        for item in setup_block.items:
            if is_setup_context(item.context_expr):
                assert has_hide_code(item.context_expr), f"app.setup in {notebook_name} must hide its source"

    app_functions = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and any(app_decorator_name(decorator) in {"cell", "function"} for decorator in node.decorator_list)
    ]
    assert app_functions, f"{notebook_name} must define Marimo app cells"
    for function in app_functions:
        decorators = [
            decorator for decorator in function.decorator_list if app_decorator_name(decorator) in {"cell", "function"}
        ]
        assert any(has_hide_code(decorator) for decorator in decorators), (
            f"{function.name} in {notebook_name} must hide its source"
        )
