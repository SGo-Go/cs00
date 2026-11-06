# Lecture assets

Lecture materials are grouped by lecture.
Each lecture folder can contain a README and a `notebooks/` directory:

```text
assets/
├── README.md
└── lectureNN/
    ├── README.md
    └── notebooks/
        └── example.py
```

`lectureNN` and `example.py` illustrate the naming pattern rather than literal paths.
Consult each lecture's README for its notebooks and molab links.

## Interactive notebooks

- **Run:** Use `uv run marimo edit path/to/notebook.py` from the repository root, or open a molab `/wasm` link.
- **Author:** Keep notebooks self-contained with marimo and the Python standard library; molab/WASM does not install local workspace packages.
- **Imports:** Put imports in `with app.setup(hide_code=True):`, except for the `import marimo` bootstrap.
- **Test:** Run `uv run pytest tests/test_notebooks.py` to execute notebooks without editable workspace packages.
