# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Lecture 1: counting in binary."""

from manim import (
    DOWN,
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

from cs00_visuals.style import ACCENT, FONT, HEX, MUTED, OFF, ON, TEXT


def bit_string(number: int, width: int) -> str:
    """Return `number` as a zero-padded binary string of `width` digits."""
    return format(number, f"0{width}b")


def hex_digit(number: int) -> str:
    """Return `number` in base 16 using upper-case digits, e.g. 10 -> `A`."""
    return format(number, "X")


class BinaryCounting(Scene):
    """Count from 0 to 15 and show each number as four bits, in decimal, and as one base-16 digit."""

    bits = 4

    def construct(self) -> None:
        """Build the animation."""
        title = Text("Двійковий лічильник", font=FONT, color=TEXT).to_edge(UP)
        cells = VGroup(*(Square(side_length=1.2) for _ in range(self.bits))).arrange(RIGHT, buff=0.25)
        weights = VGroup(
            *(
                Text(str(2**power), font=FONT, font_size=28, color=MUTED).next_to(cell, UP)
                for power, cell in zip(range(self.bits - 1, -1, -1), cells, strict=True)
            )
        )

        digits = self._digits(0, cells)
        value = self._value(0, cells)
        self.play(Write(title))
        self.play(FadeIn(cells), FadeIn(weights), FadeIn(digits), FadeIn(value))

        for number in range(1, 2**self.bits):
            new_digits = self._digits(number, cells)
            new_value = self._value(number, cells)
            self.play(
                ReplacementTransform(digits, new_digits),
                ReplacementTransform(value, new_value),
                run_time=0.4,
            )
            digits, value = new_digits, new_value
            self.wait(0.2)

        self.wait()

    def _digits(self, number: int, cells: VGroup) -> VGroup:
        """Place one digit in each cell; ones are highlighted."""
        return VGroup(
            *(
                Text(bit, font=FONT, font_size=56, color=ON if bit == "1" else OFF).move_to(cell)
                for bit, cell in zip(bit_string(number, self.bits), cells, strict=True)
            )
        )

    def _value(self, number: int, cells: VGroup) -> VGroup:
        """Show the value under the cells in base 10 and in base 16."""
        decimal = Text(f"= {number}₁₀", font=FONT, font_size=48, color=ACCENT)
        hexadecimal = Text(f"= {hex_digit(number)}₁₆", font=FONT, font_size=48, color=HEX)
        return VGroup(decimal, hexadecimal).arrange(RIGHT, buff=1.0).next_to(cells, DOWN, buff=0.6)
