# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Lecture 1: how a float32 number is stored as sign, exponent, and mantissa bits."""

import struct
from typing import NamedTuple

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    ReplacementTransform,
    Scene,
    Square,
    Text,
    VGroup,
    Write,
)

from cs00.scenes.style import ACCENT, EXPONENT, FONT, MANTISSA, MUTED, SIGN, TEXT

BIAS = 127
MANTISSA_BITS = 23
MINUS = "\N{MINUS SIGN}"
TIMES = "\N{MULTIPLICATION SIGN}"
SUPERSCRIPT = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


class Float32Parts(NamedTuple):
    """Bit fields of an IEEE 754 single-precision number."""

    sign: str
    exponent: str
    mantissa: str


def float32_parts(value: float) -> Float32Parts:
    """Split `value`, rounded to float32, into its 1 sign, 8 exponent, and 23 mantissa bits."""
    (raw,) = struct.unpack(">I", struct.pack(">f", value))
    bits = format(raw, "032b")
    return Float32Parts(bits[0], bits[1:9], bits[9:])


def float32_stored(value: float) -> float:
    """Return the value that float32 actually stores for `value`."""
    (stored,) = struct.unpack(">f", struct.pack(">f", value))
    return float(stored)


def superscript(number: int) -> str:
    """Write an integer with superscript digits, e.g. -3 -> `⁻³`."""
    return str(number).translate(SUPERSCRIPT)


class FloatingPoint(Scene):
    """Decode float32 numbers bit by bit and show that 0.1 is stored only approximately."""

    values = (6.25, -0.75, 0.1)

    def construct(self) -> None:
        """Build the animation."""
        title = Text("Число з рухомою комою: float32", font=FONT, font_size=40, color=TEXT).to_edge(UP)
        sign_cells = self._cells(1, SIGN)
        exponent_cells = self._cells(8, EXPONENT)
        mantissa_cells = self._cells(MANTISSA_BITS, MANTISSA)
        cells = VGroup(sign_cells, exponent_cells, mantissa_cells).arrange(RIGHT, buff=0.2).shift(UP * 0.9)
        labels = VGroup(
            *(
                Text(text, font=FONT, font_size=20, color=color).next_to(group, UP, buff=0.15)
                for text, color, group in (
                    ("знак", SIGN, sign_cells),
                    ("порядок", EXPONENT, exponent_cells),
                    ("мантиса", MANTISSA, mantissa_cells),
                )
            )
        )

        self.play(Write(title))
        self.play(FadeIn(cells), FadeIn(labels))

        view = self._view(self.values[0], cells)
        self.play(FadeIn(view))
        self.wait(2)
        for value in self.values[1:]:
            new_view = self._view(value, cells)
            self.play(ReplacementTransform(view, new_view))
            view = new_view
            self.wait(2)
        self.wait()

    @staticmethod
    def _cells(count: int, color: str) -> VGroup:
        """Draw `count` empty bit cells outlined in `color`."""
        return VGroup(*(Square(side_length=0.34, color=color) for _ in range(count))).arrange(RIGHT, buff=0.04)

    def _view(self, value: float, cells: VGroup) -> VGroup:
        """Show the bits of `value` in the cells and the decoding steps below them."""
        parts = float32_parts(value)
        boxes = [box for group in cells for box in group]
        digits = VGroup(
            *(
                Text(bit, font=FONT, font_size=20, color=TEXT if bit == "1" else MUTED).move_to(box)
                for bit, box in zip(parts.sign + parts.exponent + parts.mantissa, boxes, strict=True)
            )
        )

        exponent = int(parts.exponent, 2) - BIAS
        significand = 1 + int(parts.mantissa, 2) / 2**MANTISSA_BITS
        sign = MINUS if parts.sign == "1" else "+"
        steps = VGroup(
            Text(f"знак: {sign}", font=FONT, font_size=26, color=SIGN),
            Text(
                f"порядок: {int(parts.exponent, 2)} {MINUS} {BIAS} = {str(exponent).replace('-', MINUS)}",
                font=FONT,
                font_size=26,
                color=EXPONENT,
            ),
            Text(f"мантиса: 1 + дріб = {significand:.10g}", font=FONT, font_size=26, color=MANTISSA),
            Text(
                f"{sign}{significand:.10g} {TIMES} 2{superscript(exponent)} = {float32_stored(value):.17g}",
                font=FONT,
                font_size=30,
                color=ACCENT,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        steps.next_to(cells, DOWN, buff=0.7)

        header = Text(f"x = {value}", font=FONT, font_size=34, color=ACCENT).next_to(cells, UP, buff=0.75)
        return VGroup(header, digits, steps)
