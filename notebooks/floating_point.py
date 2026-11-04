# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Interactive IEEE 754 decoder: how float16, float32, and float64 store a number."""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")

with app.setup:
    import struct
    from decimal import Decimal, InvalidOperation

    import marimo as mo


@app.cell
def _():
    mo.md(r"""
    # Числа з рухомою комою

    Комп'ютер зберігає дробове число як три поля бітів за стандартом IEEE 754:

    - **знак**: 0 для додатних чисел, 1 для від'ємних;
    - **порядок**: степінь двійки, записаний зі зсувом;
    - **мантиса**: дробова частина числа виду 1,… у двійковій системі.

    Значення дорівнює $(-1)^{\text{знак}} \times 1{,}\text{мантиса}_2 \times 2^{\text{порядок} - \text{зсув}}$.
    """)
    return


@app.cell
def _():
    # struct format, exponent bits, mantissa bits
    FORMATS = {
        "float16 (половинна точність)": ("e", 5, 10),
        "float32 (одинарна точність)": ("f", 8, 23),
        "float64 (подвійна точність)": ("d", 11, 52),
    }
    COLORS = {"sign": "#c62828", "exponent": "#1565c0", "mantissa": "#2e7d32"}
    return COLORS, FORMATS


@app.cell
def _(FORMATS):
    precision = mo.ui.dropdown(options=FORMATS, value="float32 (одинарна точність)", label="Формат")
    number = mo.ui.text(value="0.1", label="Число")
    mo.hstack([number, precision], justify="start", gap=2)
    return number, precision


@app.cell
def _(number, precision):
    fmt, exponent_bits, mantissa_bits = precision.value
    total_bits = 1 + exponent_bits + mantissa_bits
    bias = 2 ** (exponent_bits - 1) - 1

    problem = ""
    try:
        typed = float(number.value.replace(",", "."))
        packed = struct.pack(f">{fmt}", typed)
    except ValueError:
        packed = None
        problem = "Введіть число, наприклад `0.1`, `-6.25` або `1e-3`."
    except OverflowError:
        packed = None
        problem = "Число завелике для цього формату: воно перевищує найбільше скінченне значення."

    mo.stop(packed is None, mo.callout(mo.md(problem), kind="warn"))

    (stored,) = struct.unpack(f">{fmt}", packed)
    bits = format(int.from_bytes(packed, "big"), f"0{total_bits}b")
    sign_bits, exponent_field, mantissa_field = bits[0], bits[1 : 1 + exponent_bits], bits[1 + exponent_bits :]
    return (
        bias,
        bits,
        exponent_bits,
        exponent_field,
        mantissa_bits,
        mantissa_field,
        sign_bits,
        stored,
    )


@app.cell
def _(COLORS, bits, exponent_bits):
    def bit_cell(bit: str, color: str) -> str:
        background = color if bit == "1" else "white"
        text = "white" if bit == "1" else color
        return (
            f'<span style="display:inline-block;width:1.4em;height:1.6em;line-height:1.6em;margin:1px;'
            f"text-align:center;font-family:monospace;border:2px solid {color};border-radius:4px;"
            f'background:{background};color:{text}">{bit}</span>'
        )

    def field(label: str, field_bits: str, color: str) -> str:
        cells = "".join(bit_cell(bit, color) for bit in field_bits)
        return (
            '<div style="display:inline-block;vertical-align:top;margin:4px 8px">'
            f'<div style="color:{color};font-size:0.85em">{label} ({len(field_bits)})</div>{cells}</div>'
        )

    fields = (
        field("знак", bits[0], COLORS["sign"]),
        field("порядок", bits[1 : 1 + exponent_bits], COLORS["exponent"]),
        field("мантиса", bits[1 + exponent_bits :], COLORS["mantissa"]),
    )
    mo.Html(f"<div>{''.join(fields)}</div>")
    return


@app.cell
def _(
    bias,
    exponent_bits,
    exponent_field,
    mantissa_bits,
    mantissa_field,
    number,
    sign_bits,
    stored,
):
    raw_exponent = int(exponent_field, 2)
    fraction = int(mantissa_field, 2) / 2**mantissa_bits
    sign_text = "−" if sign_bits == "1" else "+"

    if raw_exponent == 2**exponent_bits - 1:
        kind = "нескінченність" if int(mantissa_field, 2) == 0 else "NaN (не число)"
        formula = f"порядок складається з одиниць, тож це {kind}"
    elif raw_exponent == 0:
        kind = "нуль" if int(mantissa_field, 2) == 0 else "субнормальне число"
        formula = f"{sign_text}{fraction:.12g} \\times 2^{{{1 - bias}}}"
    else:
        kind = "нормальне число"
        formula = f"{sign_text}{1 + fraction:.12g} \\times 2^{{{raw_exponent} - {bias}}} = {sign_text}{1 + fraction:.12g} \\times 2^{{{raw_exponent - bias}}}"

    exact = Decimal(stored)
    try:
        error = Decimal(number.value.replace(",", ".")) - exact
        error_text = f"`{error:.3E}`" if error else "`0`, число зберігається точно"
    except InvalidOperation:
        error_text = "—"

    mo.md(f"""
    | Поле | Значення |
    | ---- | -------- |
    | Тип | {kind} |
    | Знак | `{sign_bits}` → {sign_text} |
    | Порядок | `{exponent_field}` = {raw_exponent}, зсув {bias} |
    | Мантиса | `{mantissa_field}` |
    | Формула | ${formula}$ |
    | Збережене значення | `{exact}` |
    | Похибка відносно введеного | {error_text} |
    """)
    return


@app.cell
def _():
    total = 0.1 + 0.2
    mo.md(f"""
    ## Чому `0.1 + 0.2 != 0.3`

    Ні 0,1, ні 0,2 не мають скінченного двійкового запису, тому зберігаються наближено:

    | Вираз | Точне збережене значення (float64) |
    | ----- | ---------------------------------- |
    | `0.1` | `{Decimal.from_float(0.1)}` |
    | `0.2` | `{Decimal.from_float(0.2)}` |
    | `0.1 + 0.2` | `{Decimal(total)}` |
    | `0.3` | `{Decimal.from_float(0.3)}` |

    У Python `0.1 + 0.2 == 0.3` дає `{total == 0.3}`.
    Тому дробові числа порівнюють з допуском, наприклад через `math.isclose(0.1 + 0.2, 0.3)`.
    """)
    return


if __name__ == "__main__":
    app.run()
