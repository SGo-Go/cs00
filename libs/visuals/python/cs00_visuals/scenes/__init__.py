# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Registry of scenes rendered for the course site."""

from manim import Scene

from .lecture01_binary import BinaryCounting
from .lecture01_float import FloatingPoint

SCENES: tuple[type[Scene], ...] = (BinaryCounting, FloatingPoint)
