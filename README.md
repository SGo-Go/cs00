# CS00: Prep course for CS50 (in Ukrainian)

<div align="center">

[![Website](https://img.shields.io/website?url=https%3A%2F%2Fsgo-go.github.io%2Fcs00%2F&up_message=online&down_message=offline&label=website)](https://sgo-go.github.io/cs00/)
[![Publish site](https://github.com/SGo-Go/cs00/actions/workflows/publish-site.yml/badge.svg)](https://github.com/SGo-Go/cs00/actions/workflows/publish-site.yml)
[![Issues](https://img.shields.io/github/issues/SGo-Go/cs00)](https://github.com/SGo-Go/cs00/issues)
[![Last commit](https://img.shields.io/github/last-commit/SGo-Go/cs00)](https://github.com/SGo-Go/cs00/commits)
[![License](https://img.shields.io/github/license/SGo-Go/cs00)](LICENSE)

</div>

<!-- [![Built with Quarto](https://img.shields.io/badge/built%20with-Quarto-447099)](https://quarto.org/) -->

## Repository layout

| Path | Description |
| --- | --- |
| `libs/cs00/` | Core Python library shared by all assignments |
| `assignments/assignment-00/` | Library for assignment 0 (depends on `cs00`) |
| `docs/quarto/` | Course website |
| `docs/sphinx/` | API reference of the Python libraries |

The Python packages form a [uv workspace](https://docs.astral.sh/uv/concepts/projects/workspaces/) defined in the root `pyproject.toml`.
Each package keeps its sources in `python/` and its tests in `tests/`.

To add an assignment, copy `assignments/assignment-00/` to `assignments/assignment-NN/` and rename the project and module.
Then add the new package to `dependencies` and `[tool.uv.sources]` in the root `pyproject.toml`.
Finish with `uv sync --inexact` and `pytest libs assignments`.

To build the API reference, run the following from the repository root:

```sh
uv sync --inexact --group docs
sphinx-build -W -b html docs/sphinx docs/sphinx/_build/html
```

New packages are added to `docs/sphinx/api.rst`.
