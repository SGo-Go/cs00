# Матеріали лекції 1

Інтерактивні зошити доповнюють [конспект лекції](../../docs/quarto/lectures/01-data-encoding.qmd).

## Структура

```text
lecture01/
├── README.md
└── notebooks/
    ├── binary_counter.py
    ├── caesar_cipher.py
    ├── floating_point.py
    └── huffman_coding.py
```

Сцени для анімацій розташовані окремо в [cs00.scenes.data_encoding](../../libs/cs00/python/cs00/scenes/data_encoding/).

## Інтерактивні зошити

| Зошит | Тема | Відкрити в molab |
| --- | --- | --- |
| [Двійковий лічильник](notebooks/binary_counter.py) | Біти та системи числення | [Відкрити](https://molab.marimo.io/github/SGo-Go/cs00/blob/main/assets/lecture01/notebooks/binary_counter.py/wasm) |
| [Шифр Цезаря](notebooks/caesar_cipher.py) | Зсув, шифрування та розшифрування | [Відкрити](https://molab.marimo.io/github/SGo-Go/cs00/blob/main/assets/lecture01/notebooks/caesar_cipher.py/wasm) |
| [Числа з рухомою комою](notebooks/floating_point.py) | Формати float16/32/64 та похибки | [Відкрити](https://molab.marimo.io/github/SGo-Go/cs00/blob/main/assets/lecture01/notebooks/floating_point.py/wasm) |
| [Кодування Гаффмана](notebooks/huffman_coding.py) | Префіксні коди та стискання тексту | [Відкрити](https://molab.marimo.io/github/SGo-Go/cs00/blob/main/assets/lecture01/notebooks/huffman_coding.py/wasm) |

Для локального запуску з кореня репозиторію, наприклад:

```sh
uv run marimo edit assets/lecture01/notebooks/binary_counter.py
```
