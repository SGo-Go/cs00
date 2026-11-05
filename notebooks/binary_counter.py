# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Interactive binary and hexadecimal counter for lecture 1."""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import marimo as mo


@app.cell
def _():
    mo.md("""
    # Двійковий лічильник

    Оберіть число й подивіться, як воно записується бітами.
    Кожні чотири біти утворюють одну шістнадцяткову цифру.
    """)
    return


@app.cell
def _():
    width = mo.ui.dropdown(options={"4 біти": 4, "8 бітів": 8}, value="8 бітів", label="Кількість бітів")
    width
    return (width,)


@app.cell
def _(width):
    number = mo.ui.slider(0, 2**width.value - 1, value=min(42, 2**width.value - 1), label="Число", show_value=True)
    number
    return (number,)


@app.cell
def _(number, width):
    ON, OFF, HEX = "#2e7d32", "#cfd8dc", "#1565c0"

    def bit_box(bit: str, weight: int) -> str:
        background = ON if bit == "1" else OFF
        color = "white" if bit == "1" else "#455a64"
        return (
            '<div style="display:inline-flex;flex-direction:column;align-items:center;margin:2px">'
            f'<span style="font-size:0.8em;color:#78909c">{weight}</span>'
            f'<span style="width:2.2em;height:2.2em;line-height:2.2em;text-align:center;font-size:1.4em;'
            f'font-family:monospace;border-radius:6px;background:{background};color:{color}">{bit}</span>'
            "</div>"
        )

    bits = format(number.value, f"0{width.value}b")
    nibbles = [bits[start : start + 4] for start in range(0, len(bits), 4)]
    groups = []
    for index, nibble in enumerate(nibbles):
        first_power = width.value - 1 - 4 * index
        boxes = "".join(bit_box(bit, 2 ** (first_power - offset)) for offset, bit in enumerate(nibble))
        digit = format(int(nibble, 2), "X")
        groups.append(
            '<div style="display:inline-flex;flex-direction:column;align-items:center;margin:0 10px">'
            f"<div>{boxes}</div>"
            f'<span style="font-size:1.6em;font-family:monospace;color:{HEX}">{digit}</span>'
            "</div>"
        )
    mo.Html(f'<div style="display:flex;justify-content:center">{"".join(groups)}</div>')
    return


@app.cell
def _(number, width):
    value = number.value
    mo.md(
        f"""
        | Основа | Запис |
        | ------ | ----- |
        | 10 | `{value}` |
        | 2 | `{format(value, f"0{width.value}b")}` |
        | 16 | `{format(value, "X")}` |
        | 8 | `{format(value, "o")}` |
        """
    )
    return


@app.cell
def _():
    mo.vstack(
        [
            mo.md("## Таблиця для чисел від 0 до 15"),
            mo.ui.table(
                [{"10": value, "2": format(value, "04b"), "16": format(value, "X")} for value in range(16)],
                selection=None,
                pagination=False,
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
