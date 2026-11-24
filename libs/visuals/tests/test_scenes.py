# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Tests for the course visualizations."""

from pathlib import Path

import pytest
from cs00.scenes.data_encoding.binary import BinaryCounting, bit_string, hex_digit
from cs00.scenes.data_encoding.floating_point import (
    Float32Parts,
    FloatingPoint,
    float32_parts,
    float32_stored,
    superscript,
)
from cs00.scenes.data_encoding.modular import IntegerModuloCircle
from cs00_visuals.render import render_scene, slug
from cs00_visuals.scenes import SCENES
from manim import Dot, Scene


@pytest.mark.parametrize(("number", "expected"), [(0, "0"), (9, "9"), (10, "A"), (15, "F")])
def test_hex_digit(number: int, expected: str) -> None:
    """Use upper-case base-16 digits."""
    assert hex_digit(number) == expected


@pytest.mark.parametrize(("number", "expected"), [(0, "0000"), (5, "0101"), (15, "1111")])
def test_bit_string(number: int, expected: str) -> None:
    """Pad binary strings to a fixed width."""
    assert bit_string(number, 4) == expected


def test_slug() -> None:
    """Derive kebab-case file names from scene class names."""
    assert slug(BinaryCounting) == "binary-counting"


@pytest.mark.parametrize("movie", [False, True])
def test_render_scene_groups_media(tmp_path: Path, movie: bool) -> None:
    """Write generated media into type-specific folders below a lecture."""

    class RenderProbe(Scene):
        """Minimal scene used to test rendered output paths."""

        def construct(self) -> None:
            self.add(Dot())
            self.wait(0.1)

    output = tmp_path / "lecture01"
    output.mkdir()
    result = render_scene(RenderProbe, output, "draft", movie=movie)
    expected = output / ("video" if movie else "img") / ("render-probe.mp4" if movie else "render-probe.png")
    assert result == expected
    assert result.stat().st_size > 0


def test_scene_names_are_unique() -> None:
    """Keep output file names unique."""
    names = [slug(scene) for scene in SCENES]
    assert len(names) == len(set(names))


def test_registry_uses_data_encoding_scenes() -> None:
    """Keep the renderer connected to the public scene classes."""
    assert BinaryCounting in SCENES
    assert FloatingPoint in SCENES
    assert IntegerModuloCircle in SCENES


def test_float32_parts_of_one() -> None:
    """Store 1.0 as a zero sign, the bias as exponent, and an empty fraction."""
    assert float32_parts(1.0) == Float32Parts("0", "01111111", "0" * 23)


def test_float32_parts_of_negative_three_quarters() -> None:
    """Store -0.75 = -1.5 x 2^-1."""
    assert float32_parts(-0.75) == Float32Parts("1", "01111110", "1" + "0" * 22)


def test_float32_stores_one_tenth_approximately() -> None:
    """Round 0.1 to the nearest float32."""
    assert float32_stored(0.1) == 0.10000000149011612
    assert float32_stored(6.25) == 6.25


def test_superscript() -> None:
    """Write exponents with superscript digits."""
    assert superscript(-3) == "⁻³"
    assert superscript(10) == "¹⁰"
