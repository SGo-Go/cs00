# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Interactive Caesar cipher with a cipher wheel, letter mapping, and brute-force decryption."""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")

with app.setup:
    import math

    import marimo as mo


@app.cell
def _():
    mo.md("""
    # Шифр Цезаря

    Кожна літера замінюється літерою, що стоїть на кілька позицій далі в алфавіті.
    Після останньої літери рахунок продовжується з початку, як на циферблаті.
    Інші символи, наприклад пробіли й розділові знаки, не змінюються.
    """)
    return


@app.cell
def _():
    ALPHABETS = {
        "Українська": "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ",
        "English": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    }

    def caesar(text: str, shift: int, alphabet: str) -> str:
        """Shift every letter of `alphabet` in `text` by `shift` positions, keeping case and other symbols."""
        size = len(alphabet)
        result = []
        for char in text:
            upper = char.upper()
            if upper in alphabet:
                shifted = alphabet[(alphabet.index(upper) + shift) % size]
                result.append(shifted if char.isupper() else shifted.lower())
            else:
                result.append(char)
        return "".join(result)

    return ALPHABETS, caesar


@app.cell
def _(ALPHABETS):
    language = mo.ui.dropdown(options=ALPHABETS, value="Українська", label="Алфавіт")
    mode = mo.ui.radio(options={"Зашифрувати": 1, "Розшифрувати": -1}, value="Зашифрувати", label="Дія")
    mo.hstack([language, mode], justify="start", gap=2)
    return language, mode


@app.cell
def _(language):
    default_text = "Привіт, світе!" if language.selected_key == "Українська" else "Hello, world!"
    shift = mo.ui.slider(0, len(language.value) - 1, value=3, label="Зсув", show_value=True)
    message = mo.ui.text_area(value=default_text, label="Текст", full_width=True)
    mo.vstack([shift, message])
    return message, shift


@app.cell
def _(caesar, language, message, mode, shift):
    result = caesar(message.value, mode.value * shift.value, language.value)
    mo.md(f"""
    **Результат:**

    ```text
    {result}
    ```
    """)
    return (result,)


@app.cell
def _(language, message, shift):
    def wheel(alphabet: str, offset: int, used: set[str]) -> str:
        """Draw two letter rings: the outer one plain, the inner one shifted by `offset`."""
        size, center = len(alphabet), 210
        parts = [
            f'<svg viewBox="0 0 {2 * center} {2 * center}" width="380" xmlns="http://www.w3.org/2000/svg"'
            ' font-family="DejaVu Sans, sans-serif" text-anchor="middle" dominant-baseline="central">',
            f'<circle cx="{center}" cy="{center}" r="195" fill="#eceff1"/>',
            f'<circle cx="{center}" cy="{center}" r="150" fill="#cfd8dc"/>',
            f'<circle cx="{center}" cy="{center}" r="105" fill="white"/>',
        ]
        for index, letter in enumerate(alphabet):
            angle = 2 * math.pi * index / size - math.pi / 2
            highlight = letter in used
            for radius, char, color in (
                (172, letter, "#c62828" if highlight else "#37474f"),
                (127, alphabet[(index + offset) % size], "#1565c0" if highlight else "#607d8b"),
            ):
                x, y = center + radius * math.cos(angle), center + radius * math.sin(angle)
                weight = "bold" if highlight else "normal"
                parts.append(
                    f'<text x="{x:.1f}" y="{y:.1f}" font-size="17" font-weight="{weight}" fill="{color}">{char}</text>'
                )
        parts.append(f'<text x="{center}" y="{center}" font-size="34" fill="#37474f">+{offset}</text>')
        parts.append("</svg>")
        return "".join(parts)

    used_letters = {char.upper() for char in message.value} & set(language.value)
    mo.vstack(
        [
            mo.md("## Шифрувальний круг"),
            mo.md("Зовнішнє кільце — звичайні літери, внутрішнє — їхні заміни. Літери з тексту виділено."),
            mo.Html(
                f'<div style="display:flex;justify-content:center">{wheel(language.value, shift.value, used_letters)}</div>'
            ),
        ]
    )
    return


@app.cell
def _(language, shift):
    alphabet = language.value
    shifted = alphabet[shift.value :] + alphabet[: shift.value]
    cell = "padding:2px 5px;text-align:center;font-family:monospace;border:1px solid #cfd8dc"
    rows = "".join(
        f"<tr><th style='{cell}'>{label}</th>"
        + "".join(f"<td style='{cell}'>{char}</td>" for char in letters)
        + "</tr>"
        for label, letters in (("Відкритий", alphabet), ("Шифр", shifted))
    )
    mo.vstack(
        [
            mo.md("## Таблиця заміни"),
            mo.Html(f"<div style='overflow-x:auto'><table style='border-collapse:collapse'>{rows}</table></div>"),
        ]
    )
    return


@app.cell
def _(caesar, language, result):
    mo.vstack(
        [
            mo.md("""
    ## Злам перебором

    Ключів лише стільки, скільки літер в алфавіті, тож можна просто спробувати всі зсуви.
    Серед варіантів легко помітити осмислений текст.
    """),
            mo.ui.table(
                [
                    {"Зсув": key, "Розшифровка": caesar(result, -key, language.value)}
                    for key in range(len(language.value))
                ],
                selection=None,
                pagination=False,
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
