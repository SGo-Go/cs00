# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Interactive Huffman coding with a prefix tree and lossless decoding."""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import heapq
    from collections import Counter
    from html import escape
    from typing import NamedTuple

    import marimo as mo

    class HuffmanNode(NamedTuple):
        """A leaf symbol or the combined weight of two subtrees."""

        weight: int
        symbol: str | None = None
        left: "HuffmanNode | None" = None
        right: "HuffmanNode | None" = None

    class HeapEntry(NamedTuple):
        """A priority-queue entry with a deterministic tie breaker."""

        weight: int
        order: int
        node: HuffmanNode

    class CodePath(NamedTuple):
        """A tree node and its path from the root."""

        node: HuffmanNode
        code: str

    class HuffmanResult(NamedTuple):
        """The tree, codebook, encoded payload, and source frequencies."""

        root: HuffmanNode | None
        codes: dict[str, str]
        bits: str
        frequencies: Counter[str]

    class Position(NamedTuple):
        """The center of a node in the SVG tree."""

        x: float
        y: float


@app.function(hide_code=True)
def huffman_encode(text: str) -> HuffmanResult:
    """Build deterministic prefix codes by merging the two least frequent nodes."""
    frequencies = Counter(text)
    queue = [
        HeapEntry(count, order, HuffmanNode(count, symbol))
        for order, (symbol, count) in enumerate(sorted(frequencies.items()))
    ]
    heapq.heapify(queue)
    order = len(queue)
    while len(queue) > 1:
        left = heapq.heappop(queue).node
        right = heapq.heappop(queue).node
        parent = HuffmanNode(left.weight + right.weight, left=left, right=right)
        heapq.heappush(queue, HeapEntry(parent.weight, order, parent))
        order += 1

    root = queue[0].node if queue else None
    codes: dict[str, str] = {}
    pending = [CodePath(root, "")] if root is not None else []
    while pending:
        node, code = pending.pop()
        if node.symbol is not None:
            codes[node.symbol] = code or "0"
        else:
            if node.right is not None:
                pending.append(CodePath(node.right, code + "1"))
            if node.left is not None:
                pending.append(CodePath(node.left, code + "0"))
    return HuffmanResult(root, codes, "".join(codes[symbol] for symbol in text), frequencies)


@app.function(hide_code=True)
def huffman_decode(bits: str, root: HuffmanNode | None) -> str:
    """Decode a bit stream, rejecting invalid digits, paths, and incomplete codes."""
    if any(bit not in "01" for bit in bits):
        raise ValueError("Код має містити лише 0 та 1.")
    if root is None:
        if bits:
            raise ValueError("Немає дерева для декодування непорожнього коду.")
        return ""
    if root.symbol is not None:
        if "1" in bits:
            raise ValueError("Для єдиного символу використовується лише код 0.")
        return root.symbol * len(bits)

    decoded: list[str] = []
    node = root
    for bit in bits:
        child = node.left if bit == "0" else node.right
        if child is None:
            raise ValueError("Код не відповідає дереву.")
        node = child
        if node.symbol is not None:
            decoded.append(node.symbol)
            node = root
    if node is not root:
        raise ValueError("Послідовність закінчилася посеред коду символу.")
    return "".join(decoded)


@app.function(hide_code=True)
def symbol_label(symbol: str) -> str:
    """Make whitespace and invisible characters recognizable in the table and tree."""
    labels = {" ": "пробіл", "\n": r"\n", "\t": r"\t", "\r": r"\r"}
    return labels.get(symbol, symbol if symbol.isprintable() else ascii(symbol))


@app.function(hide_code=True)
def huffman_tree_svg(root: HuffmanNode | None) -> str:
    """Draw a scrollable prefix tree with escaped symbol labels and 0/1 edges."""
    if root is None:
        return '<svg xmlns="http://www.w3.org/2000/svg" role="img"><title>Порожнє дерево</title></svg>'

    edges: list[str] = []
    nodes: list[str] = []
    leaf_index = 0
    max_depth = 0

    def visit(node: HuffmanNode, depth: int) -> Position:
        nonlocal leaf_index, max_depth
        max_depth = max(max_depth, depth)
        children: list[Position] = []
        for child in (node.left, node.right):
            if child is not None:
                children.append(visit(child, depth + 1))
        if children:
            x = sum(child.x for child in children) / len(children)
        else:
            x = 70 + 120 * leaf_index
            leaf_index += 1
        position = Position(x, 40 + depth * 100)
        for bit, child in zip(("0", "1"), children, strict=False):
            edges.append(
                f'<line x1="{x}" y1="{position.y}" x2="{child.x}" y2="{child.y}" stroke="#78909c"/>'
                f'<text x="{(x + child.x) / 2 + (10 if bit == "1" else -10)}"'
                f' y="{(position.y + child.y) / 2}" fill="#1565c0">{bit}</text>'
            )
        fill = "#e3f2fd" if node.symbol is not None else "#eceff1"
        label = f"{symbol_label(node.symbol)}: {node.weight}" if node.symbol is not None else str(node.weight)
        nodes.append(
            f'<rect x="{x - 52}" y="{position.y - 20}" width="104" height="40" rx="8"'
            f' fill="{fill}" stroke="#607d8b"/>'
            f'<text x="{x}" y="{position.y + 5}" fill="#263238">{escape(label)}</text>'
        )
        return position

    visit(root, 0)
    width, height = max(240, leaf_index * 120 + 20), max_depth * 100 + 80
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"'
        f' viewBox="0 0 {width} {height}" role="img" aria-label="Дерево кодування Гаффмана"'
        ' font-family="DejaVu Sans, sans-serif" font-size="14" text-anchor="middle">'
        "<title>Дерево Гаффмана: ліве ребро 0, праве ребро 1</title>" + "".join(edges) + "".join(nodes) + "</svg>"
    )


@app.cell(hide_code=True)
def _():
    mo.md("""
    # Кодування Гаффмана

    Часті символи можна записати короткими кодами, а рідкісні — довшими.
    Змініть текст і простежте, як частоти визначають дерево та кількість бітів.
    Це **стискання без втрат**, а не шифрування: секретного ключа тут немає.

    Алгоритм щоразу об'єднує два вузли з найменшими частотами.
    Частота нового вузла дорівнює їхній сумі; об'єднання тривають до єдиного кореня.
    """)
    return


@app.cell(hide_code=True)
def _():
    message = mo.ui.text_area(
        value="абракадабра",
        label="Текст для кодування (до 2000 символів)",
        debounce=500,
        full_width=True,
    )
    message
    return (message,)


@app.cell(hide_code=True)
def _(message):
    mo.stop(
        len(message.value) > 2000,
        mo.callout(
            mo.md("Скоротіть текст до 2000 символів, щоб дерево залишалося зручним для дослідження."), kind="warn"
        ),
    )
    result = huffman_encode(message.value)
    decoded = huffman_decode(result.bits, result.root)
    return decoded, result


@app.cell(hide_code=True)
def _(result):
    if result.root is None:
        mo.output.replace(mo.callout(mo.md("Введіть текст, щоб побудувати дерево й таблицю кодів."), kind="info"))
    else:
        mo.output.replace(
            mo.vstack(
                [
                    mo.md("## Частоти та коди"),
                    mo.ui.table(
                        [
                            {
                                "Символ": symbol_label(symbol),
                                "Частота": count,
                                "Код": result.codes[symbol],
                                "Бітів на символ": len(result.codes[symbol]),
                                "Бітів разом": count * len(result.codes[symbol]),
                            }
                            for symbol, count in sorted(
                                result.frequencies.items(), key=lambda item: (-item[1], item[0])
                            )
                        ],
                        selection=None,
                        pagination=False,
                    ),
                ]
            )
        )
    return


@app.cell(hide_code=True)
def _(result):
    mo.vstack(
        [
            mo.md("""
            ## Дерево кодів

            Почніть від кореня: ліве ребро додає `0`, праве — `1`.
            Шлях до символу утворює його код; числа у вузлах — частоти.
            Жоден код не є початком іншого, бо символи розташовані лише в листках.
            Для одного різного символу домовимося використовувати код `0`.
            Широке дерево можна прокручувати горизонтально.
            """),
            mo.Html(f'<div style="overflow-x:auto;padding:8px">{huffman_tree_svg(result.root)}</div>'),
        ]
    )
    return


@app.cell(hide_code=True)
def _(decoded, result):
    mo.vstack(
        [
            mo.md("## Кодування й відновлення"),
            mo.md("Закодовані біти:"),
            mo.Html(
                '<pre style="white-space:pre-wrap;overflow-wrap:anywhere;max-height:14em;overflow-y:auto">'
                f"{result.bits or '(порожня послідовність)'}</pre>"
            ),
            mo.md("Відновлений текст:"),
            mo.Html(f'<pre style="white-space:pre-wrap">{escape(decoded) if decoded else "(порожній текст)"}</pre>'),
            mo.callout(mo.md("Відновлений текст точно збігається з початковим."), kind="success"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(message, result):
    symbol_count = len(result.codes)
    fixed_width = max(1, (symbol_count - 1).bit_length()) if symbol_count else 0
    fixed_bits = len(message.value) * fixed_width
    utf8_bits = len(message.value.encode("utf-8")) * 8
    huffman_bits = len(result.bits)
    payload_bytes = (huffman_bits + 7) // 8
    mo.md(f"""
    ## Скільки місця займають дані

    | Спосіб запису | Бітів |
    | --- | ---: |
    | UTF-8 | {utf8_bits} |
    | Однакова довжина кодів (бітів на символ: {fixed_width}) | {fixed_bits} |
    | Гаффман: сума частот × довжин кодів | {huffman_bits} |

    Різних символів: **{symbol_count}**.
    Розмір упакованого бітового потоку в байтах: **{payload_bytes}** (з урахуванням доповнення останнього байта).
    Показані вище `0` та `1` — наочний текстовий запис, а не упаковані біти.

    **Це лише розмір корисних даних, а не готового стисненого файлу.**
    Для декодування треба також зберегти дерево або таблицю кодів і довжину бітового потоку.
    На короткому тексті ці накладні витрати можуть перевищити виграш.
    Порівняння кодів однакової довжини використовує лише символи цього повідомлення;
    UTF-8 натомість є універсальним кодуванням Unicode.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md("""
    ## Спробуйте самі

    1. Порівняйте `аааааб` та `абвгде`: як частоти впливають на довжини кодів?
    2. Залиште лише один різний символ, а потім очистьте текст.
    3. Додайте пробіли, перенесення рядка або емодзі й перевірте відновлений текст.
    4. Чому для збереження файлу недостатньо записати лише біти повідомлення?

    За однакових частот можливі різні, але однаково ефективні дерева.
    Цей зошит розв'язує такі нічиї у сталому порядку.
    Один символ тут — одна кодова точка Unicode; видимий знак іноді складається з кількох таких точок.

    Докладніше: [Код Гаффмана у Вікіпедії](https://uk.wikipedia.org/wiki/Код_Гаффмана).
    """)
    return


if __name__ == "__main__":
    app.run()
