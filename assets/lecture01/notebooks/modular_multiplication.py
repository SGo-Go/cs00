# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Interactive visualization of multiplication modulo powers of two."""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import math

    import marimo as mo
    import plotly.graph_objects as go

    def modular_product_map(modulus: int, multiplier: int) -> list[int]:
        """Return the output residue for each input under modular multiplication."""
        return [(residue * multiplier) % modulus for residue in range(modulus)]


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Множення за модулем степеня двійки[^mathologer-video]

    Кожен залишок $x$ з'єднано з результатом $(m x) \bmod N$ на колі.
    Змініть степінь $k$ або множник $m$ і спостерігайте за візерунком.
    Для непарного $m$ множення переставляє всі залишки, а парний множник згортає їх у меншу множину.

    [^mathologer-video]: [*Times Tables, Mandelbrot and the Heart of Mathematics*](https://youtu.be/qhbuKbxJsk8)
        by Mathologer.
    """)
    return


@app.cell(hide_code=True)
def _():
    exponent = mo.ui.slider(2, 10, value=8, label="Степінь k", show_value=True)
    exponent
    return (exponent,)


@app.cell(hide_code=True)
def _(exponent):
    modulus = 2**exponent.value
    multiplier = mo.ui.slider(0, modulus - 1, value=min(3, modulus - 1), label="Множник m", show_value=True)
    mo.vstack([mo.md(f"Модуль: **$N = 2^{{{exponent.value}}} = {modulus}$**"), multiplier])
    return modulus, multiplier


@app.cell(hide_code=True)
def _(modulus, multiplier):
    figure = create_modular_multiplication_figure(modulus, multiplier.value)
    figure
    return


@app.cell(hide_code=True)
def _(modulus, multiplier):
    product_residues = modular_product_map(modulus, multiplier.value)
    divisor = math.gcd(multiplier.value, modulus)
    distinct_outputs = len(set(product_residues))
    is_permutation = distinct_outputs == modulus
    mapping_description = "перестановка всіх залишків" if is_permutation else "повторює частину залишків"

    mo.md(
        f"""
        **gcd(m, N):** {divisor}<br>
        **Різних виходів:** {distinct_outputs} з {modulus}<br>
        **Властивість:** множення {mapping_description}.

        Для $N=2^k$ кількість різних виходів дорівнює $N / \\gcd(m,N)$.
        """
    )
    return


@app.function(hide_code=True)
def create_modular_multiplication_figure(modulus: int, multiplier: int) -> go.Figure:
    """Return a residue wheel for multiplication by a selected integer."""
    product_residues = modular_product_map(modulus, multiplier)
    angles = [2 * math.pi * residue / modulus - math.pi / 2 for residue in range(modulus)]
    point_x = [math.cos(angle) for angle in angles]
    point_y = [math.sin(angle) for angle in angles]
    line_x: list[float | None] = []
    line_y: list[float | None] = []

    for source_residue, target_residue in enumerate(product_residues):
        target_angle = 2 * math.pi * target_residue / modulus - math.pi / 2
        line_x.extend([point_x[source_residue], math.cos(target_angle), None])
        line_y.extend([point_y[source_residue], math.sin(target_angle), None])

    circle_angles = [2 * math.pi * step / 360 for step in range(361)]
    label_stride = max(1, modulus // 32)
    label_x = [1.12 * math.cos(angle) for angle in angles]
    label_y = [1.12 * math.sin(angle) for angle in angles]
    labels = [str(residue) if residue % label_stride == 0 else "" for residue in range(modulus)]
    hover_data = [[residue, product_residues[residue]] for residue in range(modulus)]

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=[math.cos(angle) for angle in circle_angles],
            y=[math.sin(angle) for angle in circle_angles],
            mode="lines",
            line={"color": "#8ca3a0", "width": 1},
            hoverinfo="skip",
            showlegend=False,
        )
    )
    figure.add_trace(
        go.Scatter(
            x=line_x,
            y=line_y,
            mode="lines",
            line={"color": "#e07842", "width": 1},
            hoverinfo="skip",
            showlegend=False,
        )
    )
    figure.add_trace(
        go.Scatter(
            x=point_x,
            y=point_y,
            customdata=hover_data,
            mode="markers",
            marker={"size": 7, "color": "#176b5b", "line": {"color": "white", "width": 1}},
            hovertemplate="Вхідний залишок: %{customdata[0]}<br>Результат: %{customdata[1]}<extra></extra>",
            showlegend=False,
        )
    )
    figure.add_trace(
        go.Scatter(
            x=label_x,
            y=label_y,
            text=labels,
            mode="text",
            textfont={"size": 10, "color": "#233238"},
            hoverinfo="skip",
            showlegend=False,
        )
    )
    figure.update_layout(
        title={"text": f"Множення за модулем {modulus}; m = {multiplier}", "x": 0.5},
        height=500,
        margin={"l": 24, "r": 24, "t": 60, "b": 24},
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis={"visible": False, "range": [-1.25, 1.25], "scaleanchor": "y", "scaleratio": 1},
        yaxis={"visible": False, "range": [-1.25, 1.25]},
        showlegend=False,
    )
    return figure


if __name__ == "__main__":
    app.run()
