# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Skip the visualization tests when Manim is not installed."""

import importlib.util

collect_ignore = [] if importlib.util.find_spec("manim") else ["test_scenes.py"]
