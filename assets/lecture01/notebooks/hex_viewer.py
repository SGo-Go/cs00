# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Interactive hexadecimal viewer for binary and text files."""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="full")

with app.setup(hide_code=True):
    import html

    import marimo as mo

    MAX_WINDOW_BYTES = 1024
    BYTES_PER_ROW = 16


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Переглядач файлів у шістнадцятковому форматі

    Відкрийте файл або перетягніть його в область нижче.
    Переглядач показує шістнадцяткові байти та друковані ASCII-символи.
    Для великих файлів задайте початковий зсув і розмір вікна до 1024 байтів.
    Завантаження у Marimo обмежене 100 МБ.
    """)
    return


@app.function
def format_hex_dump(data: bytes, start_offset: int = 0, byte_count: int = MAX_WINDOW_BYTES) -> str:
    """Format a bounded byte range as offset, hexadecimal bytes, and ASCII."""
    safe_offset = min(max(start_offset, 0), len(data))
    safe_count = min(max(byte_count, 0), MAX_WINDOW_BYTES)
    selected = data[safe_offset : safe_offset + safe_count]
    rows = []

    for row_start in range(0, len(selected), BYTES_PER_ROW):
        chunk = selected[row_start : row_start + BYTES_PER_ROW]
        hex_bytes = " ".join(f"{byte:02X}" for byte in chunk)
        ascii_bytes = "".join(chr(byte) if 0x20 <= byte <= 0x7E else "." for byte in chunk)
        rows.append(f"{safe_offset + row_start:08X}  {hex_bytes:<47}  |{ascii_bytes}|")

    return "\n".join(rows)


@app.cell(hide_code=True)
def _():
    file_upload = mo.ui.file(
        kind="area",
        label="Відкрийте файл або перетягніть його сюди",
        max_size=100_000_000,
    )
    file_upload
    return (file_upload,)


@app.cell(hide_code=True)
def _(file_upload):
    uploaded_file = file_upload.value[0] if file_upload.value else None
    file_name = uploaded_file.name if uploaded_file is not None else ""
    file_bytes = uploaded_file.contents if uploaded_file is not None else b""
    file_size = len(file_bytes)
    return file_bytes, file_name, file_size


@app.cell(hide_code=True)
def _(file_size):
    byte_window = mo.ui.dropdown(
        options={f"{count} байтів": count for count in (16, 32, 64, 128, 256, 512, 1024)},
        value="1024 байтів",
        label="Розмір вікна",
    )
    start_offset = mo.ui.number(
        start=0,
        stop=max(file_size - 1, 0),
        step=1,
        value=0,
        label="Початковий байт",
        disabled=file_size == 0,
    )
    mo.hstack([start_offset, byte_window], justify="start", gap=2)
    return byte_window, start_offset


@app.cell(hide_code=True)
def _(byte_window, file_bytes, file_name, file_size, start_offset):
    if not file_name:
        output = mo.callout(mo.md("Виберіть файл або перетягніть його в область вище."), kind="neutral")
    else:
        offset = int(start_offset.value or 0)
        window_size = int(byte_window.value)
        visible_bytes = file_bytes[offset : offset + window_size]
        row_header = "ЗСУВ     " + " ".join(f"{column:02X}" for column in range(BYTES_PER_ROW)) + "  ASCII\n"
        dump = format_hex_dump(file_bytes, offset, window_size)
        shown_end = offset + len(visible_bytes)
        file_info = (
            f"{html.escape(file_name)} · {file_size:,} байт · "
            f"показано {offset}–{shown_end - 1 if visible_bytes else offset} "
            f"({len(visible_bytes)} байтів)"
        )
        output = mo.Html(
            f'<p class="hex-file-info">{file_info}</p><pre class="hex-dump">{html.escape(row_header + dump)}</pre>'
        )
    output
    return


@app.cell(hide_code=True)
def _():
    mo.Html(
        """
        <style>
        .hex-file-info {
          color: #52635d;
          font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
          margin: .75rem 0 .4rem;
          overflow-wrap: anywhere;
        }
        .hex-dump {
          background: #f0f5f3;
          border: 1px solid #b8c8c1;
          border-radius: 4px;
          color: #20302b;
          font-size: .82rem;
          line-height: 1.55;
          max-height: 32rem;
          overflow: auto;
          padding: .75rem;
          white-space: pre;
        }
        </style>
        """
    )
    return


if __name__ == "__main__":
    app.run()
