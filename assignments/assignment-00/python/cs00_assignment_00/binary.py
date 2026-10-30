# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Binary representation of integers."""


def to_binary(number: int) -> str:
    """Return the binary representation of an integer.

    Args:
        number: The integer to convert.

    Returns:
        The binary digits of `number`, with a leading minus sign for negative numbers.

    """
    return format(number, "b")
