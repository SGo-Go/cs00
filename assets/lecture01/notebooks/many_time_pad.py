# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Explore why reusing a stream-cipher pad leaks message relationships."""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import marimo as mo


@app.function
def xor_bytes(left: bytes, right: bytes) -> bytes:
    """XOR equal-length byte strings, rejecting accidental truncation."""
    if len(left) != len(right):
        raise ValueError("XOR inputs must have equal lengths.")
    return bytes(left_byte ^ right_byte for left_byte, right_byte in zip(left, right, strict=True))


@app.function(hide_code=True)
def guess_other_byte_from_space(cipher_a: bytes, cipher_b: bytes, index: int) -> int | None:
    """Assume message A has a space at index and infer message B's byte."""
    if index < 0 or index >= len(cipher_a) or index >= len(cipher_b):
        return None
    return cipher_a[index] ^ cipher_b[index] ^ 0x20


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Атака на шифр Вернама за повторного використання ключа

    У цьому зошиті на навчальному прикладі розглянемо, чому небезпечно повторно використовувати ключ
    у [шифрі Вернама](https://uk.wikipedia.org/wiki/Шифр_Вернама), або одноразовому блокноті.
    Повторне використання того самого потоку ключа в XOR-шифрі розкриває зв'язок між відкритими повідомленнями.
    Джерело вправи: [CS255 Homework 1: Many Time Pad](https://cs255.stanford.edu/hw/hw1.html).
    Тут використано лише вигадані короткі повідомлення, а не дані чи відповіді з вправи.

    > Усі наведені приклади — навчальні й не призначені для захисту реальних даних.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1. XOR над байтами

    Операція XOR порівнює біти попарно: однакові дають `0`, а різні — `1`.
    У Python XOR над числами позначають оператором `^`.

    Перед шифруванням текст кодують у байти, наприклад за допомогою `message_text.encode("utf-8")`.
    Отримані байти шифротексту можна подати шістнадцятковим рядком за допомогою `.hex()`.
    XOR є операцією, оберненою до самої себе: якщо двічі застосувати той самий байт ключового потоку,
    початковий байт відновиться.
    Тож байти шифрують XOR-ом із ключовим потоком, а розшифровують повторним XOR-ом із тим самим потоком.
    """)
    return


@app.cell
def _():
    message_text = "A"
    sample_plaintext = message_text.encode("utf-8")
    sample_key_stream = bytes([0b00101010])
    sample_ciphertext = xor_bytes(sample_plaintext, sample_key_stream)
    sample_recovered = xor_bytes(sample_ciphertext, sample_key_stream)

    assert sample_recovered == sample_plaintext
    print("Рядок:", message_text)
    print("UTF-8 байти:", sample_plaintext.hex().upper())
    print("Байт ключового потоку:", sample_key_stream.hex().upper())
    print("Шифротекст:", sample_ciphertext.hex().upper())
    print("Розшифровано й декодовано:", sample_recovered.decode("utf-8"))
    return


@app.cell
def _():
    try:
        xor_bytes(b"A", b"AB")
    except ValueError as length_error:
        print("Вхідні послідовності мають різну довжину:", length_error)
    else:
        raise AssertionError("xor_bytes повинен відхиляти різну довжину аргументів.")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2. Одноразовий блокнот

    До кожного байта відкритого повідомлення застосовують XOR із відповідним байтом ключового потоку.
    Розшифрування повторює ту саму операцію з тим самим потоком.

    Криптографічно стійкий одноразовий блокнот потребує справді випадкового й секретного ключа завдовжки з повідомлення.
    Ключ має бути незалежним і використаним лише один раз.
    У наступному прикладі короткий ключ фіксований лише для відтворюваності.
    """)
    return


@app.cell
def _():
    one_time_message = b"DATA"
    demonstration_pad = bytes([0x6A, 0x2F, 0x94, 0x10])
    one_time_ciphertext = xor_bytes(one_time_message, demonstration_pad)
    one_time_recovered = xor_bytes(one_time_ciphertext, demonstration_pad)

    print("Повідомлення:", one_time_message)
    print("Демонстраційний потік ключа:", demonstration_pad.hex(" ").upper())
    print("Шифротекст:", one_time_ciphertext.hex(" ").upper())
    print("Розшифровано:", one_time_recovered)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3. Чому повторне використання ключа небезпечне

    Нехай два повідомлення зашифрували тим самим ключовим потоком `K`:
    `C₁ = M₁ XOR K` і `C₂ = M₂ XOR K`.
    Якщо виконати XOR шифротекстів, однакові ключові потоки взаємно скоротяться: `C₁ XOR C₂ = M₁ XOR M₂`.

    Сам цей результат не розкриває повідомлень, але встановлює зв'язок між їхніми символами.
    Мовні закономірності та відомі фрагменти тексту можуть допомогти висунути здогади про відкриті повідомлення.
    """)
    return


@app.cell
def _():
    toy_message_a = b"the plan is ready"
    toy_message_b = b"send secret data!"
    toy_pad = bytes((index * 37 + 19) % 256 for index in range(len(toy_message_a)))

    assert len(toy_message_a) == len(toy_message_b) == len(toy_pad)
    toy_cipher_a = xor_bytes(toy_message_a, toy_pad)
    toy_cipher_b = xor_bytes(toy_message_b, toy_pad)
    xor_of_ciphertexts = xor_bytes(toy_cipher_a, toy_cipher_b)
    xor_of_messages = xor_bytes(toy_message_a, toy_message_b)

    assert xor_of_ciphertexts == xor_of_messages
    print("Демонстраційний ключовий потік:", toy_pad.hex(" ").upper())
    print("Шифротекст A:", toy_cipher_a.hex(" ").upper())
    print("Шифротекст B:", toy_cipher_b.hex(" ").upper())
    print("A XOR B:", xor_of_ciphertexts.hex(" ").upper())
    print("Це M₁ XOR M₂, а не безпосередньо M₁ чи M₂.")
    return toy_cipher_a, toy_cipher_b, toy_message_b


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4. Що підказує пробіл

    У звичайному тексті пробіли трапляються часто.
    Якщо припустити, що на певній позиції в повідомленні A стоїть пробіл,
    байт повідомлення B можна оцінити за формулою `(C₁ XOR C₂) XOR 0x20`.

    Це лише **гіпотеза**, а не універсальний декодер.
    Перевіряйте її за сусідніми символами та мовним контекстом.
    """)
    return


@app.cell
def _(toy_cipher_a, toy_cipher_b, toy_message_b):
    guessed_position = 3
    guessed_byte = guess_other_byte_from_space(toy_cipher_a, toy_cipher_b, guessed_position)
    print("Припускаємо, що в A на позиції", guessed_position, "є пробіл.")
    if guessed_byte is None:
        print("Позиція поза межами одного з шифротекстів.")
    else:
        print("Можливий символ у B:", repr(chr(guessed_byte)), "(байт", f"0x{guessed_byte:02X}", ")")
        print("У нашому вигаданому прикладі це збігається:", guessed_byte == toy_message_b[guessed_position])

    invalid_position = len(toy_cipher_a)
    assert guess_other_byte_from_space(toy_cipher_a, toy_cipher_b, invalid_position) is None
    print("Перевірка виходу за межі:", guess_other_byte_from_space(toy_cipher_a, toy_cipher_b, invalid_position))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5. Спроба виконати вправу CS255

    На сторінці [CS255 Homework 1: Many Time Pad](https://cs255.stanford.edu/hw/hw1.html) наведено
    список шифротекстів у шістнадцятковому записі.
    Скопіюйте їхні записи до `exercise_ciphertexts_hex`, а шифротекст,
    який потрібно розшифрувати, — до `target_ciphertext_hex`.
    Клітинка перетворює непорожні hex-рядки на байти (`bytes`); якщо поля залишити порожніми,
    результатом будуть порожній список і порожній шифротекст.

    **Підказка:** порівнюйте XOR-пари шифротекстів і перевіряйте здогади про пробіли за контекстом.
    """)
    return


@app.cell
def _():
    exercise_ciphertexts_hex = []  # Вставте hex-шифротексти зі сторінки вправи.
    target_ciphertext_hex = ""  # Вставте hex цільового шифротексту.
    exercise_ciphertexts = [bytes.fromhex(value) for value in exercise_ciphertexts_hex]
    target_ciphertext = bytes.fromhex(target_ciphertext_hex) if target_ciphertext_hex else b""

    print("Кількість шифротекстів:", len(exercise_ciphertexts))
    print("Цільовий шифротекст задано:", bool(target_ciphertext))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Спробуйте далі

    Замініть вигадані повідомлення власними короткими рядками з ASCII-символів однакової довжини.
    Повторно використайте `toy_pad` і порівняйте XOR шифротекстів із XOR відкритих повідомлень.
    Знайдіть позицію, де в одному повідомленні стоїть пробіл, і перевірте здогад за контекстом.
    Не використовуйте цей демонстраційний прийом для шифрування реальних даних або захисту секретів.
    """)
    return


if __name__ == "__main__":
    app.run()
