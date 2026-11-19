# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Guided playground for Python data encoding basics."""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import tempfile
    import unicodedata
    from pathlib import Path
    from urllib.request import Request, urlopen

    import marimo as mo
    import numpy

    IMAGE_URL = "https://sgo-go.github.io/cs00/media/lecture01/img/binary-counting.png"
    IMAGE_FILE_PATH = Path(tempfile.gettempdir()) / "cs00-tryout-image.png"
    NOTEBOOK_FILE_PATH = Path(__file__).resolve()

    def download_file(url: str, destination: Path) -> str | None:
        """Download a URL to a cached file, returning an error message on failure."""
        if destination.is_file() and destination.stat().st_size > 0:
            return None

        request = Request(url, headers={"User-Agent": "CS00 data encoding playground/1.0"})
        try:
            with urlopen(request, timeout=30) as response:
                contents = response.read()
            destination.write_bytes(contents)
        except OSError as download_error:
            return str(download_error)

        return None

    IMAGE_DOWNLOAD_ERROR = download_file(IMAGE_URL, IMAGE_FILE_PATH)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Як комп'ютер зберігає текст і числа

    Цей зошит крок за кроком досліджує, як Python представляє числа, символи й байти.
    Читайте пояснення, запускайте код і змінюйте значення у видимих клітинках.

    Ми користуватимемося бібліотеками `numpy` та `unicodedata`.
    Інші потрібні інструменти — це вже вбудовані можливості Python: рядки, списки, цикли, `print` і `open`.

    Усі приклади читання файлів нижче розраховані на запуск із кореня репозиторію.
    Зошит читає файли репозиторію, а завантажене зображення зберігає в системному тимчасовому каталозі.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1. Бібліотеки та перший вивід

    **Бібліотека** — це набір готових інструментів, якими можна скористатися у програмі.
    NumPy допомагає працювати з числами фіксованої розрядності, а `unicodedata` надає відомості про символи Unicode.

    У звичайному Python імпорт виглядає так:

    ```python
    import numpy
    import unicodedata
    ```

    У цьому зошиті ці бібліотеки вже імпортовані у прихованій налаштувальній клітинці.
    Функція `print` показує текстове подання результату.
    """)
    return


@app.cell
def _():
    print("Почнімо з кодування даних!")
    print("NumPy:", numpy.__version__)
    print("Версія таблиці Unicode:", unicodedata.unidata_version)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Змінні, значення й оператори

    **Значення** — це конкретні дані, наприклад число `10`.
    **Змінна** — це ім'я, якому Python присвоює значення, щоб його можна було використати пізніше.

    Один знак `=` — це **оператор присвоєння**: Python обчислює вираз праворуч і пов'язує результат з ім'ям ліворуч.
    Два знаки `==` — це **порівняння**: воно перевіряє, чи рівні значення, і повертає `True` або `False`.
    Тому `count = 3` змінює прив'язане до `count` значення, а `count == 3` лише перевіряє його.
    """)
    return


@app.cell
def _():
    count = 3
    print("Значення змінної count:", count)
    print("Чи дорівнює count числу 3?", count == 3)
    count = count + 1
    print("Після присвоєння нового значення:", count)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2. Текстові рядки

    Рядок (`str`) — це послідовність символів у лапках.
    Одинарні та подвійні лапки працюють однаково:

    ```python
    greeting = "Привіт"
    language = 'Python'
    ```

    Щоб записати лапки всередині тексту, можна вибрати інший вид лапок або використати зворотну скісну риску.
    Символ `\n` означає перехід на новий рядок.

    Функція `type(value)` показує тип об'єкта, на який посилається змінна.
    Наприклад, тип рядка — `str`, цілого числа — `int`.
    """)
    return


@app.cell
def _():
    greeting = "Привіт, Python!"
    sentence = "Бітів у байті: 8.\nДані мають різні подання."
    print(greeting)
    print(sentence)
    print("Тип greeting:", type(greeting).__name__)
    print("Тип числа:", int.__name__)

    multiline_text = """Це перший рядок.
    Це другий рядок у тому самому рядковому значенні."""
    print("Багаторядковий рядок:")
    print(multiline_text)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3. Числові записи: десятковий, двійковий і шістнадцятковий

    Саме число можна записати різними системами числення.
    У Python префікс `0b` позначає двійковий літерал, а `0x` — шістнадцятковий.
    Звичайний запис без префікса десятковий.

    Наприклад, двійкове `0b1010`, шістнадцяткове `0xA` і десяткове `10` позначають те саме число.
    Функція `int` також уміє перетворити рядок із цифрами на число, якщо передати основу системи числення.
    """)
    return


@app.cell
def _():
    decimal_ten = 10
    binary_ten = 0b1010
    hexadecimal_ten = 0xA
    print(decimal_ten, binary_ten, hexadecimal_ten)
    print(decimal_ten == binary_ten == hexadecimal_ten)
    print(int("1010", 2), int("A", 16))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Спробуйте змінити число

    Замініть літерали на інші значення та порівняйте результати.
    Наприклад, `0b111111001010` і `0x7EA` — це два записи числа 2026.
    """)
    return


@app.cell
def _():
    tryout_number = 0x7EA
    print("Десятковий запис:", tryout_number)
    print("Двійковий запис:", format(tryout_number, "b"))
    print("Шістнадцятковий запис:", format(tryout_number, "X"))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Цикл `for` і функція `range`

    Цикл `for` послідовно бере елементи з послідовності й виконує для кожного тіло циклу.
    `range(start, stop, step)` створює послідовність цілих чисел із заданим кроком.
    Початок входить у послідовність, але `stop` не входить: `range(1, 5)` дає `1`, `2`, `3`, `4`.
    """)
    return


@app.cell
def _():
    print("Числа з range(1, 5):")
    for range_value in range(1, 5):
        print(range_value)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Умови `if` та `else`

    Умова `if` виконує свій блок, коли перевірка істинна.
    Гілка `else` виконується, коли умова хибна.
    Разом ці гілки утворюють конструкцію `if/else`.
    Відступи визначають, які рядки належать до кожного блоку.
    """)
    return


@app.cell
def _():
    score_example = 72
    if score_example >= 50:
        print("Результат:", score_example, "— умову виконано")
    else:
        print("Результат:", score_example, "— умову не виконано")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4. Списки, кортежі, індекси й зрізи

    **Список** (`list`) записують у квадратних дужках, наприклад `[1, 0, 1]`.
    Список змінюваний: після створення його елемент можна замінити або додати новий.
    **Кортеж** (`tuple`) записують у круглих дужках, наприклад `(1, 0, 1)`.
    Кортеж незмінюваний: його елементи після створення не можна переприсвоїти.
    Для кортежу з одним елементом потрібна кома: `(1,)`.

    Обидва типи зберігають значення в певному порядку, підтримують індексацію та зрізи.

    Індексація починається з нуля: перший елемент має індекс `0`, а `-1` означає останній.
    Зріз `послідовність[початок:кінець]` бере елементи від початку включно до кінця невключно.
    Ці операції однаково корисні для списків, кортежів і байтових послідовностей.
    """)
    return


@app.cell
def _():
    list_example = [1, 0, 1]
    tuple_example = (1, 0, 1)
    list_example[0] = 0
    print("Список після зміни першого елемента:", list_example)
    print("Кортеж із початковими значеннями:", tuple_example)

    bit_values = [1, 0, 1, 1, 0, 0, 1, 0]
    bit_labels = ("старший біт", "молодший біт")
    print("Список бітів:", bit_values)
    print("Перший і останній:", bit_values[0], bit_values[-1])
    print("Перші чотири:", bit_values[:4])
    print("Підпис кортежу:", bit_labels[0], "і", bit_labels[1])
    print("Кількість елементів у списку:", len(list_example))
    print("Кількість елементів у кортежі:", len(tuple_example))
    print("По одному біту:")
    for bit in bit_values:
        print(bit)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5. Функції `ord`, `chr` і `len` для роботи з символами

    `ord(character)` приймає один символ і повертає його числове значення — кодову точку Unicode.
    Наприклад, `ord("A")` дорівнює 65, а `ord("л")` — значно більше за 127.
    `chr(code_point)` виконує зворотну дію й створює символ за кодовою точкою.
    `len(text)` рахує кількість кодових точок у рядку, а не обов'язково кількість видимих знаків.
    """)
    return


@app.cell
def _():
    sample_word = "Data"
    one_letter = "A"
    ukrainian_letter = "л"
    print("Слово:", sample_word)
    print("ord('A'):", ord(one_letter))
    print("ord('л'):", ord(ukrainian_letter))
    print("chr(65):", chr(65))
    print("Кількість символів у слові:", len(sample_word))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Довжина рядка й видимий символ — не завжди одне й те саме

    Деякі видимі емодзі записані кількома кодовими точками.
    Функція `len` рахує кодові точки окремо, навіть якщо людина сприймає їх як один знак.
    """)
    return


@app.cell
def _():
    family_emoji = "👨‍👩‍👧‍👦"
    print("Видимий рядок:", family_emoji)
    print("Кількість кодових точок:", len(family_emoji))
    print("Кодові точки:")
    for family_character in family_emoji:
        print(f"U+{ord(family_character):04X}", unicodedata.name(family_character, "без назви"))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6. ASCII: перші 128 кодів

    ASCII — це історична таблиця з 128 кодами: від `0` до `127` включно.
    Вона містить керівні коди, англійські літери, цифри та розділові знаки.
    Коди `0`–`31` і `127` керівні; друковані символи займають `32`–`126`.

    У Python `ord` показує код символу, а `chr` дає змогу побачити друковану частину таблиці.
    """)
    return


@app.cell
def _():
    ascii_sample = "ASCII 2026!"
    print("Символ і десятковий код:")
    for ascii_character in ascii_sample:
        print(repr(ascii_character), ord(ascii_character))

    print("Друковані ASCII-символи від пробілу до тильди:")
    for code_point in range(32, 127):
        print(chr(code_point), end=" ")
    print()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 7. Байти: `bytes` і `bytearray`

    Байти — це числа від `0` до `255`.
    Тип `bytes` створює незмінну послідовність байтів; індексування повертає ціле число.
    Тип `bytearray` схожий на `bytes`, але його окремі байти можна змінювати.

    Щоб перетворити текст на байти, рядок кодують, наприклад методом `.encode("utf-8")`.
    Щоб відновити текст, байти декодують методом `.decode("utf-8")`.
    """)
    return


@app.cell
def _():
    ascii_bytes = bytes([0x41, 0x42, 0x43])
    print("bytes:", ascii_bytes)
    print("Перший байт як число:", ascii_bytes[0])
    print("Зріз:", ascii_bytes[:2])
    print("Шістнадцяткові байти:", ascii_bytes.hex(" ").upper())
    return


@app.cell
def _():
    editable_bytes = bytearray(b"ABC")
    editable_bytes[0] = 0x61
    print("Змінений bytearray:", editable_bytes)
    print("Декодований текст:", editable_bytes.decode("ascii"))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Текст перетворюється на байти

    Метод `.encode` повертає об'єкт `bytes`.
    Кожен елемент цього об'єкта — ціле число від `0` до `255`.
    Порівняйте кількість символів із кількістю байтів: для ASCII-літери вони однакові, але для багатьох інших літер байтів більше.
    """)
    return


@app.cell
def _():
    english_text = "A"
    ukrainian_text = "л"
    for sample_text_value in (english_text, ukrainian_text):
        encoded_value = sample_text_value.encode("utf-8")
        print(sample_text_value, "символів:", len(sample_text_value), "байтів:", len(encoded_value))
        print("Байти:", encoded_value, "hex:", encoded_value.hex(" ").upper())
        print("Назад у текст:", encoded_value.decode("utf-8"))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 8. Unicode: кодові точки символів

    Unicode призначає кодові точки символам різних писемностей, знакам та емодзі.
    Кодову точку записують як `U+` і шістнадцяткове число, наприклад `U+041B` для `Л`.

    Одна видима літера часто відповідає одній кодовій точці, але можливі винятки.
    Наприклад, літера з наголосом може бути однією готовою кодовою точкою або базовою літерою разом із комбінованим знаком.
    `unicodedata.name` показує офіційну назву кодової точки, коли вона має назву.
    """)
    return


@app.cell
def _():
    unicode_samples = ("A", "Л", "л", "ґ", "❤️")
    for unicode_sample_value in unicode_samples:
        print("Рядок:", unicode_sample_value)
        for unicode_character in unicode_sample_value:
            print(f"  U+{ord(unicode_character):04X}", unicodedata.name(unicode_character, "без назви"))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Дослідіть нормалізоване й складене написання

    Два рядки можуть виглядати однаково, але містити різні кодові точки.
    У наступному прикладі перше `é` — одна кодова точка, а друге — `e` та комбінований наголос.
    Погляньте на `len`, `ord` і назви обох послідовностей.
    """)
    return


@app.cell
def _():
    composed_text = "é"
    decomposed_text = "e\u0301"
    for label, normalization_value in (("складена форма", composed_text), ("базова літера + знак", decomposed_text)):
        print(label, repr(normalization_value), "довжина:", len(normalization_value))
        for normalization_character in normalization_value:
            print(
                f"  U+{ord(normalization_character):04X}",
                unicodedata.name(normalization_character, "без назви"),
            )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 9. UTF-8: кодування Unicode у байти

    Unicode визначає числові кодові точки; UTF-8 визначає, як записати їх у байтах.
    Кожна Unicode-кодова точка в UTF-8 займає від одного до чотирьох байтів.
    ASCII-сумісність означає, що коди `0`–`127` у UTF-8 мають ті самі значення байтів, що й в ASCII.

    Один видимий знак інколи складається з кількох кодових точок, тому він може займати більше чотирьох байтів загалом.
    """)
    return


@app.cell
def _():
    mixed_text = "Aл"
    mixed_bytes = mixed_text.encode("utf-8")
    print("Текст:", mixed_text)
    print("Кількість кодових точок:", len(mixed_text))
    print("UTF-8 як bytes:", mixed_bytes)
    print("UTF-8 як hex:", mixed_bytes.hex(" ").upper())
    print("Байти як список цілих чисел:", list(mixed_bytes))
    print("Декодування:", mixed_bytes.decode("utf-8"))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Розберіть байти одного символу циклом

    Ітерація по `bytes` повертає числа, а не рядки.
    Перетворіть кожне число на двоцифровий hex-запис і порівняйте з результатом `.hex()`.
    """)
    return


@app.cell
def _():
    letter_bytes = "л".encode()
    for byte_value in letter_bytes:
        print(byte_value, f"0x{byte_value:02X}")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 10. Цілі числа: `int` і фіксовані типи NumPy

    Python `int` зберігає цілі числа довільної точності: значення обмежене доступною пам'яттю, а не фіксованими 8 чи 16 бітами.
    Типи NumPy, наприклад `numpy.int8`, `numpy.uint8`, `numpy.int16` і `numpy.uint16`, мають фіксовану розрядність.

    Беззнакове 8-бітове число лежить у межах від `0` до `255`.
    Знакове 8-бітове число в доповненні до двійки лежить у межах від `-128` до `127`.
    `numpy.iinfo` показує межі конкретного цілого типу.
    """)
    return


@app.cell
def _():
    print("Python int може містити дуже велике ціле:", 2**100)
    integer_types = (
        numpy.int8,
        numpy.uint8,
        numpy.int16,
        numpy.uint16,
        numpy.int32,
        numpy.uint32,
        numpy.int64,
        numpy.uint64,
    )
    for integer_type in integer_types:
        type_limits = numpy.iinfo(integer_type)
        print(integer_type.__name__, "розрядність:", type_limits.bits, "межі:", type_limits.min, "…", type_limits.max)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 11. Доповнення до двійки та `astype`

    У доповненні до двійки від'ємне число займає всі біти свого типу.
    Для 8 бітів значення `-5` має бітовий запис `11111011`.
    Якщо прочитати ті самі вісім бітів як беззнакові, отримаємо `251`.

    `astype` створює масив з іншим типом NumPy.
    У прикладі число `255` після перетворення до 8-бітового знакового типу має бітовий запис `11111111`, який у доповненні до двійки означає `-1`.
    Python `int` при цьому не змінюється: зміна виникає через обмежену розрядність цільового типу.
    """)
    return


@app.cell
def _():
    negative_five = numpy.array([-5], dtype=numpy.int8)
    negative_five_bits = negative_five.view(numpy.uint8)[0]
    print("Знакове значення:", negative_five[0])
    print("Ті самі біти як unsigned:", negative_five_bits)
    print("8 бітів:", format(int(negative_five_bits), "08b"))

    source_value = numpy.uint16(0xFF)
    print("Початковий uint16:", source_value)
    print("Після astype(uint8):", source_value.astype(numpy.uint8))
    print("Після astype(int8):", source_value.astype(numpy.int8))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Відокремте бітовий запис від його тлумачення

    Масив можна подивитися як на той самий набір бітів іншого типу за допомогою `view`.
    `astype` натомість виконує перетворення значень до цільового типу.
    Для байтів `11111111` беззнакове тлумачення — `255`, а знакове тлумачення у доповненні до двійки — `-1`.
    """)
    return


@app.cell
def _():
    raw_byte = numpy.array([0b11111111], dtype=numpy.uint8)
    unsigned_interpretation = raw_byte[0]
    signed_interpretation = raw_byte.view(numpy.int8)[0]
    print("Біти:", format(int(raw_byte[0]), "08b"))
    print("uint8:", unsigned_interpretation)
    print("int8:", signed_interpretation)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 12. Шляхи та файли
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Шлях до файлу

    **Шлях до файлу** — це адреса файлу у файловій системі.
    Відносний шлях рахується від поточної папки, а абсолютний починається від кореня файлової системи.
    Модуль стандартної бібліотеки `pathlib` представляє шлях об'єктом `Path`.
    Оператор `/` поєднує частини шляху, а метод `.open()` відкриває файл.
    У Marimo `__file__` містить шлях до файлу зошита.
    `Path(__file__).resolve()` перетворює його на повний шлях, який можна відкрити методом `.open()`.
    """)
    return


@app.cell
def _():
    path_experiment = Path(__file__)
    print("Відносний шлях:", path_experiment)
    print("Абсолютний шлях:", path_experiment.resolve())
    print("Назва файлу:", path_experiment.name)
    print("Батьківська папка:", path_experiment.parent)
    print("Чи існує файл:", path_experiment.is_file())
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Читання текстового файлу

    Текстовий файл відкривають у текстовому режимі й указують кодування, зазвичай `utf-8`.
    Метод `read` повертає рядок `str`, а `with` автоматично закриває файл після читання.
    Цей приклад читає початок джерельного коду поточного зошита.
    """)
    return


@app.cell
def _():
    print("Об'єкт шляху:", type(NOTEBOOK_FILE_PATH).__name__)
    print("Шлях до зошита:", NOTEBOOK_FILE_PATH)
    with NOTEBOOK_FILE_PATH.open(encoding="utf-8") as text_file:
        text_preview = text_file.read(240)

    print("Фрагмент джерельного коду цього зошита:")
    print(text_preview)
    print("Тип результату read:", type(text_preview).__name__)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Читання бінарного файлу

    Бінарний файл відкривають у режимі `rb`, тому `read` повертає байти (`bytes`), а не текст.
    Значення байтів тлумачить програма, яка знає формат файлу.
    Під час запуску зошит завантажує зображення порядків величин у тимчасовий каталог.
    Нижче ми прочитаємо перші 16 байтів PNG-файлу та перевіримо його сигнатуру.
    """)
    return


@app.cell
def _():
    mo.stop(
        IMAGE_DOWNLOAD_ERROR is not None or not IMAGE_FILE_PATH.is_file(),
        f"Помилка завантаження зображення: {IMAGE_DOWNLOAD_ERROR}",
    )

    with IMAGE_FILE_PATH.open("rb") as image_file:
        image_header = image_file.read(16)

    print("Перші байти PNG:", image_header)
    print("Ті самі байти в hex:", image_header.hex(" ").upper())
    print("Тип результату read:", type(image_header).__name__)
    print("Сигнатура PNG:", image_header[:8] == b"\x89PNG\r\n\x1a\n")

    return


if __name__ == "__main__":
    app.run()
