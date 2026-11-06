# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Registry of scenes rendered for the course site."""

from cs00.scenes.data_encoding.binary import BinaryCounting
from cs00.scenes.data_encoding.floating_point import FloatingPoint
from manim import Scene

SCENES: tuple[type[Scene], ...] = (BinaryCounting, FloatingPoint)
