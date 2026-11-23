# Матеріали лекції 1

Інтерактивні зошити доповнюють [конспект лекції](../../docs/quarto/lectures/01-data-encoding.qmd).

## Структура

```text
lecture01/
├── README.md
└── notebooks/
    ├── binary_counter.py
    ├── caesar_cipher.py
    ├── data_encoding.py
    ├── floating_point.py
    ├── huffman_coding.py
    ├── hex_viewer.py
    ├── image_viewer.py
    ├── many_time_pad.py
    └── modular_multiplication.py
```

Сцени для анімацій розташовані окремо в [cs00.scenes.data_encoding](../../libs/cs00/python/cs00/scenes/data_encoding/).

## Інтерактивні зошити

| Зошит | Тема | Відкрити в molab |
| --- | --- | --- |
| [Двійковий лічильник](notebooks/binary_counter.py) | Біти та системи числення | [Відкрити](https://molab.marimo.io/github/SGo-Go/cs00/blob/main/assets/lecture01/notebooks/binary_counter.py/wasm) |
| [Множення за модулем степеня двійки](notebooks/modular_multiplication.py) | Відображення $x$ у $mx \bmod 2^k$ на колі залишків | [Відкрити](https://molab.marimo.io/github/SGo-Go/cs00/blob/main/assets/lecture01/notebooks/modular_multiplication.py/wasm) |
| [Hex-переглядач файлів](notebooks/hex_viewer.py) | Перегляд байтів та ASCII з вибором зміщення й розміру вікна | [Відкрити](https://molab.marimo.io/github/SGo-Go/cs00/blob/main/assets/lecture01/notebooks/hex_viewer.py/wasm) |
| [Пікселі та байти зображення](notebooks/image_viewer.py) | Масштабування, вибір ділянки та hex-байти RGB і відтінків сірого | [Відкрити](https://molab.marimo.io/github/SGo-Go/cs00/blob/main/assets/lecture01/notebooks/image_viewer.py/wasm) |
| [Кодування даних у Python](notebooks/data_encoding.py) | Числа, bytes, ASCII, Unicode, UTF-8 і читання файлів | [Відкрити](https://molab.marimo.io/github/SGo-Go/cs00/blob/main/assets/lecture01/notebooks/data_encoding.py/wasm) |
| [Шифр Цезаря](notebooks/caesar_cipher.py) | Зсув, шифрування та розшифрування | [Відкрити](https://molab.marimo.io/github/SGo-Go/cs00/blob/main/assets/lecture01/notebooks/caesar_cipher.py/wasm) |
| [Багаторазове використання потоку ключа](notebooks/many_time_pad.py) | XOR, одноразовий блокнот і витік інформації через повторне використання ключа | [Відкрити](https://molab.marimo.io/github/SGo-Go/cs00/blob/main/assets/lecture01/notebooks/many_time_pad.py/wasm) |
| [Числа з рухомою комою](notebooks/floating_point.py) | Формати float16/32/64 та похибки | [Відкрити](https://molab.marimo.io/github/SGo-Go/cs00/blob/main/assets/lecture01/notebooks/floating_point.py/wasm) |
| [Кодування Гаффмана](notebooks/huffman_coding.py) | Префіксні коди та стискання тексту | [Відкрити](https://molab.marimo.io/github/SGo-Go/cs00/blob/main/assets/lecture01/notebooks/huffman_coding.py/wasm) |

Для локального запуску з кореня репозиторію, наприклад:

```sh
uv run marimo edit assets/lecture01/notebooks/binary_counter.py
```

Переглядач зображень використовує Pillow для декодування та масштабування пікселів у Python:

```sh
uv run marimo edit --sandbox assets/lecture01/notebooks/image_viewer.py
```
