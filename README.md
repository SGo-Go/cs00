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
| `libs/visuals/` | [Manim](https://www.manim.community/) animations for lectures (`cs00-visuals`) |
| `assets/` | Lecture materials and interactive notebooks; see [assets/README.md](assets/README.md) |
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

## Rendering the course site

Install executable Quarto figure dependencies with `uv sync --inexact --group docs`.
Render the full site with executable content using `QUARTO_PYTHON="$PWD/.venv/bin/python" quarto render docs/quarto --execute`.
The publishing workflow explicitly selects this interpreter so Quarto can use the installed Jupyter dependencies.

## Lecture visualizations

Animations are written with [Manim Community](https://docs.manim.community/), the maintained fork of the 3Blue1Brown library.
Lecture 1 scenes are classes in `libs/cs00/python/cs00/scenes/data_encoding/` and are registered in `SCENES` in `libs/visuals/python/cs00_visuals/scenes/__init__.py`.

Manim builds `pycairo` and `manimpango` from source on Linux, so install the system libraries first:

```sh
sudo apt-get install libcairo2-dev libpango1.0-dev pkg-config
uv sync --inexact --group visuals
```

Render every scene to an MP4 video and a PNG still in `docs/quarto/media/visuals/`:

```sh
uv run --no-sync python -m cs00_visuals.render
```

Use `--still-only` for a quick check, `--only BinaryCounting` for one scene, and `--quality youtube` (1080p60) or `--quality 4k` for upload-ready videos.
Rendered files are gitignored, and the publish workflow renders them before building the site.

Lectures show the video on the web and the still in the PDF:

```markdown
::: {.content-visible when-format="html"}
{{< video ../media/visuals/binary-counting.mp4 >}}
:::

::: {.content-visible unless-format="html"}
![Description](../media/visuals/binary-counting.png)
:::
```

Without Manim, `quarto render` writes grey placeholder stills so the PDFs still build.
