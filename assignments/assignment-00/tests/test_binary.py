# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Tests for assignment 0."""

import pytest
from cs00_assignment_00.binary import to_binary


@pytest.mark.parametrize(("number", "expected"), [(0, "0"), (1, "1"), (5, "101"), (255, "11111111"), (-5, "-101")])
def test_to_binary(number: int, expected: str) -> None:
    """Convert integers to binary strings."""
    assert to_binary(number) == expected
