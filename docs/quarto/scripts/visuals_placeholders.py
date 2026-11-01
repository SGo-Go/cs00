# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Quarto pre-render hook: write placeholder PNGs for Manim stills that are not rendered yet.

Typst fails on missing images, so PDF builds need every referenced still to exist.
CI renders the real stills before Quarto runs, and existing files are never overwritten.
Only the standard library is used, so the hook works without Manim installed.
"""

import re
import struct
import zlib
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
STILL = re.compile(r"media/visuals/[\w-]+\.png")
WIDTH, HEIGHT = 320, 180
GREY = (69, 71, 90)


def _chunk(kind: bytes, data: bytes) -> bytes:
    """Build one PNG chunk with length and CRC."""
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))


def placeholder_png() -> bytes:
    """Return a solid grey RGB PNG."""
    row = b"\x00" + bytes(GREY) * WIDTH
    header = struct.pack(">IIBBBBB", WIDTH, HEIGHT, 8, 2, 0, 0, 0)
    return b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            _chunk(b"IHDR", header),
            _chunk(b"IDAT", zlib.compress(row * HEIGHT)),
            _chunk(b"IEND", b""),
        ]
    )


def main() -> None:
    """Create a placeholder for every referenced still that does not exist."""
    referenced = {match for qmd in PROJECT.rglob("*.qmd") for match in STILL.findall(qmd.read_text("utf-8"))}
    for relative in sorted(referenced):
        target = PROJECT / relative
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(placeholder_png())
            print(f"Placeholder written: {relative} (render it with `python -m cs00_visuals.render`)")


if __name__ == "__main__":
    main()
