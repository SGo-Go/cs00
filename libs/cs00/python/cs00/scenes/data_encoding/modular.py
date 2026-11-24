# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Lecture 1: integers on a number line wrap into modular residue classes."""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    TAU,
    UP,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    Scene,
    Text,
    Transform,
    VGroup,
    Write,
)

from cs00.scenes.style import ACCENT, FONT, MUTED, TEXT

MODULI = (8,)
INTEGER_AXIS_RANGE = (-8, 15)
RESIDUE_COLORS = (
    "#f38ba8",
    "#fab387",
    "#f9e2af",
    "#a6e3a1",
    "#94e2d5",
    "#89b4fa",
    "#cba6f7",
    "#f5c2e7",
)
CIRCLE_RADIUS = 2.0
CIRCLE_CENTER = DOWN * 0.25
MINUS = "\N{MINUS SIGN}"


def _residue_color(value: int) -> str:
    return RESIDUE_COLORS[value % MODULI[0]]


def _residue_representatives(pmod: int) -> list[tuple[int, int, int]]:
    return [(residue - pmod, residue, residue + pmod) for residue in range(pmod)]


def _residue_equivalence_list(pmod: int) -> VGroup:
    heading = Text(f"Класи за модулем {pmod}", font=FONT, font_size=22, color=TEXT)
    rows = VGroup(
        *(
            Text(
                f"{negative} ≡ {core} ≡ {positive} (mod {pmod})",
                font=FONT,
                font_size=20,
                color=_residue_color(core),
            )
            for negative, core, positive in _residue_representatives(pmod)
        )
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    return VGroup(heading, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(LEFT * 4.65 + CIRCLE_CENTER)


def _circle_point(residue: int, pmod: int, radius: float) -> np.ndarray:
    angle = PI / 2 - TAU * residue / pmod
    return np.array(
        [radius * np.cos(angle), radius * np.sin(angle) - 0.25, 0.0],
    )


def _residue_labels(pmod: int, *, color_by_class: bool = False) -> VGroup:
    stride = max(1, pmod // 16)
    return VGroup(
        *(
            Text(
                str(residue),
                font=FONT,
                font_size=20,
                color=_residue_color(residue) if color_by_class else TEXT,
            ).move_to(
                _circle_point(residue, pmod, CIRCLE_RADIUS + 0.42),
            )
            for residue in range(0, pmod, stride)
        )
    )


def _number_line_point(value: int) -> np.ndarray:
    minimum, maximum = INTEGER_AXIS_RANGE
    x = -5.3 + (value - minimum) * 10.6 / (maximum - minimum)
    return np.array([x, -0.25, 0.0])


def _number_line_residue_classes(pmod: int) -> VGroup:
    return VGroup(
        *(
            VGroup(
                *(
                    Dot(_number_line_point(value), radius=0.045, color=_residue_color(value))
                    for value in range(INTEGER_AXIS_RANGE[0], INTEGER_AXIS_RANGE[1] + 1)
                    if value % pmod == residue
                )
            )
            for residue in range(pmod)
        )
    )


def _map_residue_classes_to_circle(class_dots: VGroup, pmod: int) -> VGroup:
    return VGroup(
        *(
            VGroup(
                *(
                    Dot(_circle_point(residue, pmod, CIRCLE_RADIUS), radius=0.045, color=_residue_color(residue))
                    for _ in range(len(residue_dots))
                )
            )
            for residue, residue_dots in enumerate(class_dots)
        )
    )


class IntegerModuloCircle(Scene):
    """Demonstrate the modulo-8 equivalence classes of integers from -8 to 15.

    The number-line points are colored by residue. After the baseline, ticks,
    and labels fade, the axis and its residue-colored point groups morph
    together into a circle. The ending shows all eight representative chains
    to the left of the circle. ``animation_speed`` scales the scene timings;
    its default of 1.0 slows the animation.
    """

    animation_speed: float = 1.0

    def construct(self) -> None:
        """Build the axis-to-circle morph and display the eight equivalences."""
        (pmod_8,) = MODULI
        title = Text("Від цілих чисел до класів лишків", font=FONT, font_size=38, color=TEXT).to_edge(UP)
        axis = Line(LEFT * 5.3 + CIRCLE_CENTER, RIGHT * 5.3 + CIRCLE_CENTER, color=MUTED)
        axis_ticks = VGroup(
            *(
                Line(
                    _number_line_point(value) + UP * 0.08,
                    _number_line_point(value) + DOWN * 0.08,
                    color=MUTED,
                )
                for value in range(INTEGER_AXIS_RANGE[0], INTEGER_AXIS_RANGE[1] + 1)
            )
        )
        axis_labels = VGroup(
            *(
                Text(str(value), font=FONT, font_size=18, color=TEXT).next_to(
                    _number_line_point(value),
                    DOWN,
                    buff=0.12,
                )
                for value in (-8, -4, 0, 4, 8, 12, 15)
            )
        )
        class_dots = _number_line_residue_classes(pmod_8)
        number_line = VGroup(axis, class_dots)
        caption = Text(f"Цілі числа від {MINUS}8 до 15", font=FONT, font_size=28, color=ACCENT).to_edge(
            DOWN,
            buff=0.35,
        )

        self.play(Write(title), run_time=0.8 / self.animation_speed)
        self.play(
            Create(number_line),
            FadeIn(axis_ticks),
            FadeIn(axis_labels),
            Write(caption),
            run_time=1.4 / self.animation_speed,
        )
        self.wait(0.8 / self.animation_speed)

        circle = Circle(radius=CIRCLE_RADIUS, color=MUTED, stroke_width=2).move_to(CIRCLE_CENTER)
        circle_with_classes = VGroup(circle, _map_residue_classes_to_circle(class_dots, pmod_8))
        self.play(
            axis.animate.set_opacity(0),
            FadeOut(axis_ticks),
            FadeOut(axis_labels),
            run_time=0.6 / self.animation_speed,
        )
        self.play(
            Transform(number_line, circle_with_classes),
            run_time=3.0 / self.animation_speed,
        )
        self.wait(0.6 / self.animation_speed)

        residues8 = VGroup(
            *(
                Dot(_circle_point(residue, pmod_8, CIRCLE_RADIUS), radius=0.06, color=_residue_color(residue))
                for residue in range(pmod_8)
            )
        )
        labels8 = _residue_labels(pmod_8, color_by_class=True)
        equivalence_list = _residue_equivalence_list(pmod_8)
        self.play(
            FadeOut(number_line[1]),
            FadeIn(residues8),
            FadeIn(labels8),
            FadeOut(caption),
            FadeIn(equivalence_list),
            run_time=1.4 / self.animation_speed,
        )
        self.wait(2 / self.animation_speed)
