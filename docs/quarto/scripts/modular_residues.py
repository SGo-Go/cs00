# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Build the interactive modular-residue figure used in lecture 1."""

from typing import NamedTuple

import plotly.graph_objects as go

PMODS = tuple(2**exponent for exponent in range(1, 9))
LABEL_RADIUS = 1.18
INTEGER_BIT_WIDTHS = tuple(range(2, 9))
INTEGER_AXIS_BASE_OPACITY = 0.75

INTEGER_AXIS_HOVER_SCRIPT = """
const graph = document.getElementById('{plot_id}');
const traceIndexes = [0, 1];
graph.on('plotly_hover', (event) => {
    const residue = event.points[0].customdata[4];
    const opacities = graph.data.map((trace) =>
        trace.customdata.map((point) => point[4] === residue ? 1 : 0.12)
    );
    Plotly.restyle(graph, {'marker.opacity': opacities}, traceIndexes);
});
graph.on('plotly_unhover', () => {
    const opacities = graph.data.map((trace) => trace.customdata.map(() => 0.78));
    Plotly.restyle(graph, {'marker.opacity': opacities}, traceIndexes);
});
"""


class _IntegerAxisData(NamedTuple):
    values: list[int]
    colors: list[str]
    unsigned_symbols: list[str]
    signed_symbols: list[str]
    unsigned_customdata: list[list[int | str]]
    signed_customdata: list[list[int | str]]
    tick_values: list[int]
    axis_range: list[float]


def _integer_axis_data(bits: int) -> _IntegerAxisData:
    modulus = 2**bits
    values = list(range(-modulus, 2 * modulus))
    residues = [value % modulus for value in values]
    colors = [f"hsl({residue * 360 / modulus:.1f}, 65%, 48%)" for residue in residues]
    bit_width_hex = (bits + 3) // 4
    binary_values = [format(residue, f"0{bits}b") for residue in residues]
    hex_values = [format(residue, f"0{bit_width_hex}X") for residue in residues]
    signed_values = [residue - modulus if residue >= modulus // 2 else residue for residue in residues]
    unsigned_symbols = ["circle" if 0 <= value < modulus else "circle-open" for value in values]
    signed_symbols = ["circle" if -(modulus // 2) <= value < modulus // 2 else "circle-open" for value in values]
    unsigned_customdata = [
        [value, binary_value, hex_value, modulus, residue, residue, signed_value]
        for value, binary_value, hex_value, modulus, residue, signed_value in zip(
            values, binary_values, hex_values, [modulus] * len(values), residues, signed_values, strict=True
        )
    ]
    tick_stride = max(1, modulus // 4)
    tick_values = list(range(-modulus, 2 * modulus, tick_stride))
    axis_range = [-modulus - 0.5, 2 * modulus - 0.5]
    return _IntegerAxisData(
        values,
        colors,
        unsigned_symbols,
        signed_symbols,
        unsigned_customdata,
        unsigned_customdata,
        tick_values,
        axis_range,
    )


def _point_data(
    pmod: int, repr_min: int = -1, repr_max: int = 2
) -> tuple[list[float], list[float], list[str], list[list[int]]]:
    residues = list(range(pmod))
    angles = [360.0 * residue / pmod for residue in residues]
    radii = [1.0] * pmod
    label_stride = max(1, pmod // 16)
    labels = [str(residue) if residue % label_stride == 0 else "" for residue in residues]
    representatives = [[residue + r * pmod for r in range(repr_min, repr_max + 1)] for residue in residues]
    return angles, radii, labels, representatives


def _modulus_slider_steps(repr_min: int, repr_max: int) -> list[dict[str, object]]:
    steps: list[dict[str, object]] = []
    for current_pmod in PMODS:
        step_angles, step_radii, step_labels, step_examples = _point_data(
            current_pmod, repr_min=repr_min, repr_max=repr_max
        )
        steps.append(
            {
                "label": str(current_pmod),
                "method": "update",
                "args": [
                    {
                        "theta": [step_angles, step_angles],
                        "r": [step_radii, [LABEL_RADIUS] * current_pmod],
                        "text": [step_labels, step_labels],
                        "customdata": [step_examples, step_examples],
                    },
                    {"title.text": f"Класи лишків за модулем {current_pmod}"},
                    [1, 2],
                ],
            }
        )
    return steps


def create_modular_residue_figure(pmod: int = 16, repr_min: int = -1, repr_max: int = 2) -> go.Figure:
    """Build the interactive residue-class figure for the unsigned-integer lesson.

    Args:
        pmod: Initial modulus, one of the powers of two from 2 through 256.
            The default is 16.
        repr_min: First representative's modulus multiple, inclusive. Defaults to -1.
        repr_max: Last representative's modulus multiple, inclusive. Defaults to 2.

    Returns:
        A Plotly figure with a modulus slider, fixed-size circular points, up
        to 16 evenly spaced labels outside the circle, and hover details with
        all representatives from ``repr_min`` through ``repr_max``. The
        representative at multiplier zero is bold.

    Raises:
        ValueError: If ``pmod`` is unsupported or the representative range is
            unordered or does not include zero.

    """
    if pmod not in PMODS:
        raise ValueError(f"pmod must be one of {PMODS}")
    if repr_min > 0 or repr_max < 0 or repr_min > repr_max:
        raise ValueError("representative multipliers must be ordered and include zero")

    angles, radii, labels, examples = _point_data(pmod, repr_min=repr_min, repr_max=repr_max)
    core_index = -repr_min
    hover_fields = [f"%{{customdata[{index}]}}" for index in range(repr_max - repr_min + 1)]
    hover_fields[core_index] = f"<b>{hover_fields[core_index]}</b>"
    hovertemplate = f"Представники: {', '.join(hover_fields)}<extra></extra>"

    figure = go.Figure()
    figure.add_trace(
        go.Scatterpolar(
            r=[1.0] * 361,
            theta=list(range(361)),
            mode="lines",
            line={"color": "#68736f", "width": 1},
            hoverinfo="skip",
            showlegend=False,
        )
    )
    figure.add_trace(
        go.Scatterpolar(
            r=radii,
            theta=angles,
            customdata=examples,
            mode="markers",
            marker={"symbol": "circle", "size": 6, "color": "#d8ebe4", "line": {"color": "#176b5b", "width": 1.5}},
            hovertemplate=hovertemplate,
            showlegend=False,
        )
    )
    figure.add_trace(
        go.Scatterpolar(
            r=[LABEL_RADIUS] * pmod,
            theta=angles,
            text=labels,
            mode="text",
            textposition="middle center",
            textfont={"size": 11, "color": "#172b27"},
            hoverinfo="skip",
            showlegend=False,
        )
    )

    figure.update_layout(
        title={"text": f"Класи лишків за модулем {pmod}", "x": 0.5},
        height=480,
        margin={"l": 30, "r": 30, "t": 65, "b": 80},
        polar={
            "radialaxis": {"visible": False, "range": [0, 1.28]},
            "angularaxis": {"visible": False, "rotation": 90, "direction": "clockwise"},
        },
        sliders=[
            {
                "active": PMODS.index(pmod),
                "currentvalue": {"prefix": "Модуль p = "},
                "pad": {"t": 36},
                "steps": _modulus_slider_steps(repr_min, repr_max),
            }
        ],
    )
    return figure


def create_integer_axis_figure(bits: int = 4) -> go.Figure:
    """Build an interactive unsigned and two's-complement number-line figure.

    Args:
        bits: Bit width to display initially. Supported values are 3 through 8.

    Returns:
        A Plotly figure with unsigned and signed lanes, a bit-width slider,
        and markers colored by their residue class.

    Raises:
        ValueError: If ``bits`` is outside the supported range.

    """
    if bits not in INTEGER_BIT_WIDTHS:
        raise ValueError(f"bits must be in the range 3 through 8, got {bits}")

    axis_data = _integer_axis_data(bits)
    point_count = len(axis_data.values)
    base_opacity = [INTEGER_AXIS_BASE_OPACITY] * point_count
    hovertemplate = (
        "Число на осі: %{customdata[0]}<br>"
        "Бітове подання: %{customdata[1]} (0x%{customdata[2]})<br>"
        "Клас за модулем %{customdata[3]}: %{customdata[4]}<br>"
        "Беззнакове: %{customdata[5]}<br>"
        "Знакове: %{customdata[6]}<extra></extra>"
    )

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=axis_data.values,
            y=[1] * point_count,
            customdata=axis_data.unsigned_customdata,
            mode="markers",
            marker={
                "color": axis_data.colors,
                "opacity": base_opacity,
                "size": 9,
                "symbol": axis_data.unsigned_symbols,
                "line": {"color": "#ffffff", "width": 1},
            },
            name="Беззнакове",
            hovertemplate=hovertemplate,
            showlegend=False,
        )
    )
    figure.add_trace(
        go.Scatter(
            x=axis_data.values,
            y=[0] * point_count,
            customdata=axis_data.signed_customdata,
            mode="markers",
            marker={
                "color": axis_data.colors,
                "opacity": base_opacity,
                "size": 9,
                "symbol": axis_data.signed_symbols,
                "line": {"color": "#ffffff", "width": 1},
            },
            name="Доповнення до двійки",
            hovertemplate=hovertemplate,
            showlegend=False,
        )
    )

    steps: list[dict[str, object]] = []
    for current_bits in INTEGER_BIT_WIDTHS:
        current_data = _integer_axis_data(current_bits)
        current_count = len(current_data.values)
        current_opacity = [INTEGER_AXIS_BASE_OPACITY] * current_count
        steps.append(
            {
                "label": str(current_bits),
                "method": "update",
                "args": [
                    {
                        "x": [current_data.values, current_data.values],
                        "y": [[1] * current_count, [0] * current_count],
                        "customdata": [current_data.unsigned_customdata, current_data.signed_customdata],
                        "marker.color": [current_data.colors, current_data.colors],
                        "marker.opacity": [current_opacity, current_opacity],
                        "marker.symbol": [current_data.unsigned_symbols, current_data.signed_symbols],
                    },
                    {
                        "title.text": _integer_axis_title(current_bits),
                        "xaxis.range": current_data.axis_range,
                        "xaxis.tickvals": current_data.tick_values,
                    },
                ],
            }
        )

    figure.update_layout(
        title={"text": _integer_axis_title(bits), "x": 0.5},
        height=440,
        margin={"l": 145, "r": 25, "t": 75, "b": 95},
        xaxis={
            "title": "Число на осі",
            "range": axis_data.axis_range,
            "tickmode": "array",
            "tickvals": axis_data.tick_values,
            "zeroline": True,
            "zerolinecolor": "#68736f",
            "gridcolor": "#e4e9e7",
        },
        yaxis={
            "range": [-0.55, 1.55],
            "tickmode": "array",
            "tickvals": [1, 0],
            "ticktext": ["Беззнакове", "Доповнення до двійки"],
            "showgrid": False,
            "zeroline": False,
        },
        sliders=[
            {
                "active": INTEGER_BIT_WIDTHS.index(bits),
                "currentvalue": {"prefix": "Кількість бітів: "},
                "pad": {"t": 30},
                "steps": steps,
            }
        ],
    )
    return figure


def _integer_axis_title(bits: int) -> str:
    """Return the title for a bit width and its corresponding modulus."""
    return f"{bits}-бітові числа: класи за модулем {2**bits}"
