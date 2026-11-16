# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Build the interactive modular-residue figure used in lecture 1."""

import plotly.graph_objects as go

PMODS = tuple(2**exponent for exponent in range(1, 9))
LABEL_RADIUS = 1.18


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

    steps = []
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
                "steps": steps,
            }
        ],
    )
    return figure
