"""Автопроверка банка S02-M06 — только для преподавателя.

Запуск из каталога S02-M06/instructor:
    python3.14 verify_exercises.py

Скрипт проверяет контракт, а не конкретную реализацию: любая функция,
которая возвращает ожидаемые значения и соблюдает запреты задачи, подходит.
Ожидаемые значения в таблицах заданы независимо от reference_solutions.py;
для E17, E25, E29 и E31 дополнительно используется встроенный оракул.
"""

from reference_solutions import (
    ascii_guard,
    ascii_safe,
    byte_or_char,
    char_at,
    censor,
    codepoint_label,
    drop_last,
    edge_report,
    fit_message,
    format_receipt,
    has_extension,
    initials,
    is_palindrome,
    last_char,
    manual_count,
    mask_card,
    normalize_and_mark,
    parse_pairs,
    parse_tags,
    position_or_none,
    reformat_records,
    replace_limited,
    reverse_and_skip,
    rotate,
    round_trip,
    shift_letters,
    slice_like,
    trim_around,
    width_counts,
    words_to_dashes,
)


CASES = []


def add(task, function, args, expected):
    CASES.append((task, function, args, expected))


# E15
add("E15", edge_report, ("Кот",), "3|К|т")
add("E15", edge_report, ("x",), "1|x|x")
add("E15", edge_report, ("😀",), "1|😀|😀")
add("E15", edge_report, ("",), "0|-|-")
add("E15", edge_report, ("e\u0301",), "2|e|\u0301")
add("E15", edge_report, ("ab",), "2|a|b")

# E16
add("E16", codepoint_label, ("A",), "A=0x41")
add("E16", codepoint_label, ("я",), "я=0x44f")
add("E16", codepoint_label, ("😀",), "😀=0x1f600")
add("E16", codepoint_label, ("",), "invalid")
add("E16", codepoint_label, ("ab",), "invalid")
add("E16", codepoint_label, ("\u0301",), "\u0301=0x301")
add("E16", codepoint_label, ("é",), "é=0xe9")
add("E16", codepoint_label, ("漢",), "漢=0x6f22")

# E17
add("E17", is_palindrome, ("шалаш",), True)
add("E17", is_palindrome, ("абба",), True)
add("E17", is_palindrome, ("abca",), False)
add("E17", is_palindrome, ("",), True)
add("E17", is_palindrome, ("а",), True)
add("E17", is_palindrome, ("аб",), False)
add("E17", is_palindrome, ("Абба",), False)
add("E17", is_palindrome, ("e\u0301",), False)
add("E17", is_palindrome, ("abba",), True)
add("E17", is_palindrome, ("abcba",), True)

# E18
add("E18", char_at, ("Кот", 0), "ok:К")
add("E18", char_at, ("Кот", -1), "ok:т")
add("E18", char_at, ("Кот", 2), "ok:т")
add("E18", char_at, ("Кот", -3), "ok:К")
add("E18", char_at, ("Кот", 3), "missing")
add("E18", char_at, ("Кот", -4), "missing")
add("E18", char_at, ("", 0), "missing")
add("E18", char_at, ("", -1), "missing")
add("E18", char_at, ("😀", -1), "ok:😀")

# E19
add("E19", shift_letters, ("ABC", 1), "BCD")
add("E19", shift_letters, ("XYZ", 3), "ABC")
add("E19", shift_letters, ("Hello, World!", -1), "Gello, Vorld!")
add("E19", shift_letters, ("AZ", 26), "AZ")
add("E19", shift_letters, ("AZ", -27), "ZY")
add("E19", shift_letters, ("Кот", 5), "Кот")
add("E19", shift_letters, ("", 7), "")
add("E19", shift_letters, ("abc", 1), "abc")
add("E19", shift_letters, ("Z", 1), "A")
add("E19", shift_letters, ("A", -1), "Z")
add("E19", shift_letters, ("A1z!", 1), "B1z!")

# E20
add("E20", last_char, ("Кот",), "т")
add("E20", last_char, ("a",), "a")
add("E20", last_char, ("",), "")
add("E20", last_char, ("e\u0301",), "\u0301")

# E21
add("E21", reverse_and_skip, ("abcdef",), "fedcba|ace")
add("E21", reverse_and_skip, ("Кот",), "тоК|Кт")
add("E21", reverse_and_skip, ("",), "|")
add("E21", reverse_and_skip, ("a",), "a|a")
add("E21", reverse_and_skip, ("ab",), "ba|a")
add("E21", reverse_and_skip, ("😀a",), "a😀|😀")

# E22
add("E22", mask_card, ("1234567812345678",), "1234********5678")
add("E22", mask_card, ("123456789",), "1234*6789")
add("E22", mask_card, ("12345678",), "12345678")
add("E22", mask_card, ("1234567",), "*******")
add("E22", mask_card, ("",), "")
add("E22", mask_card, ("1234 5678 1234 5678",), "1234***********5678")
add("E22", mask_card, ("123456789012345",), "1234*******2345")

# E23
add("E23", rotate, ("abcdef", 2), "cdefab")
add("E23", rotate, ("abcdef", 0), "abcdef")
add("E23", rotate, ("abcdef", 6), "abcdef")
add("E23", rotate, ("abcdef", 8), "cdefab")
add("E23", rotate, ("abcdef", -1), "fabcde")
add("E23", rotate, ("", 5), "")
add("E23", rotate, ("a", 100), "a")
add("E23", rotate, ("Кот", 1), "отК")
add("E23", rotate, ("abcdef", -7), "fabcde")

# E24
add("E24", trim_around, ("abcdef", 2, 1), "cde")
add("E24", trim_around, ("abcdef", 0, 0), "abcdef")
add("E24", trim_around, ("abcdef", 1, 1), "bcde")
add("E24", trim_around, ("abcdef", 3, 3), "")
add("E24", trim_around, ("abcdef", 4, 4), "")
add("E24", trim_around, ("", 0, 0), "")
add("E24", trim_around, ("abc", 10, 0), "")
add("E24", trim_around, ("abc", 0, 10), "")
add("E24", trim_around, ("abcdef", 2, 10), "")
add("E24", trim_around, ("😀ab", 1, 1), "a")

# E25: документированные случаи; исчерпывающая сверка ниже.
add("E25", slice_like, ("abcdef", 1, 4, None), "bcd")
add("E25", slice_like, ("abcdef", None, None, -1), "fedcba")
add("E25", slice_like, ("abcdef", 4, 1, -1), "edc")
add("E25", slice_like, ("abcdef", None, None, 2), "ace")
add("E25", slice_like, ("abcdef", None, None, -2), "fdb")
add("E25", slice_like, ("abcdef", -4, -1, None), "cde")
add("E25", slice_like, ("abcdef", 100, None, None), "")
add("E25", slice_like, ("abcdef", 2, 2, None), "")
add("E25", slice_like, ("abcdef", None, None, 0), None)
add("E25", slice_like, ("", 0, None, -1), "")
add("E25", slice_like, ("abc", -100, None, -1), "")
add("E25", slice_like, ("abc", None, -100, -1), "cba")
add("E25", slice_like, ("abcdef", None, -2, None), "abcd")
add("E25", slice_like, ("abcdef", -2, None, None), "ef")

# E26
add("E26", drop_last, ("Кот",), "Ко")
add("E26", drop_last, ("abcdef",), "abcde")
add("E26", drop_last, ("a",), "")
add("E26", drop_last, ("",), "")
add("E26", drop_last, ("e\u0301",), "e")
add("E26", drop_last, ("😀",), "")

# E27
add("E27", censor, ("кот и кот", "кот"), "*** и ***")
add("E27", censor, ("абракадабра", "бра"), "а***када***")
add("E27", censor, ("Кот и кот", "кот"), "Кот и ***")
add("E27", censor, ("abc", "x"), "abc")
add("E27", censor, ("", "a"), "")
add("E27", censor, ("аа", "а"), "**")
add("E27", censor, ("aaaa", "aa"), "****")

# E28
add("E28", has_extension, ("report.csv", ".csv"), True)
add("E28", has_extension, ("report.csv", ".txt"), False)
add("E28", has_extension, ("REPORT.CSV", ".csv"), False)
add("E28", has_extension, ("report.csv.bak", ".csv"), False)
add("E28", has_extension, ("", ".csv"), False)
add("E28", has_extension, (".csv", ".csv"), True)
add("E28", has_extension, ("a.csv", ".csv"), True)
add("E28", has_extension, ("a.csv ", ".csv"), False)

# E29
add("E29", manual_count, ("aaaa", "aa"), 2)
add("E29", manual_count, ("абракадабра", "бра"), 2)
add("E29", manual_count, ("abc", "x"), 0)
add("E29", manual_count, ("aaa", "aa"), 1)
add("E29", manual_count, ("abc", "abc"), 1)
add("E29", manual_count, ("", "a"), 0)
add("E29", manual_count, ("abababa", "aba"), 2)
add("E29", manual_count, ("aaaaa", "aa"), 2)
add("E29", manual_count, ("😀😀😀", "😀😀"), 1)

# E30
add("E30", normalize_and_mark, (" hi! ",), "hi")
add("E30", normalize_and_mark, ("hi",), "hi")
add("E30", normalize_and_mark, ("hi!x",), "hi!x")
add("E30", normalize_and_mark, ("!",), "")
add("E30", normalize_and_mark, ("hi!!",), "hi!")
add("E30", normalize_and_mark, ("",), "")
add("E30", normalize_and_mark, ("  ",), "")
add("E30", normalize_and_mark, ("\tкот!\n",), "кот")
add("E30", normalize_and_mark, ("!!!",), "!!")

# E31
add("E31", replace_limited, ("aaaa", "aa", "b", -1), "bb")
add("E31", replace_limited, ("aaaa", "aa", "b", 1), "baa")
add("E31", replace_limited, ("aaaa", "aa", "b", 0), "aaaa")
add("E31", replace_limited, ("abc", "x", "y", -1), "abc")
add("E31", replace_limited, ("Кот", "о", "О", 1), "КОт")
add("E31", replace_limited, ("aaa", "aa", "b", -1), "ba")
add("E31", replace_limited, ("", "a", "b", -1), "")
add("E31", replace_limited, ("abab", "ab", "X", 2), "XX")
add("E31", replace_limited, ("abc", "abc", "", -1), "")
add("E31", replace_limited, ("abc", "b", "BB", -1), "aBBc")
add("E31", replace_limited, ("banana", "na", "NA", 2), "baNANA")
add("E31", replace_limited, ("aaaa", "a", "aa", 2), "aaaaaa")

# E32
add("E32", position_or_none, ("абракадабра", "бра"), 1)
add("E32", position_or_none, ("abc", "x"), None)
add("E32", position_or_none, ("abc", ""), 0)
add("E32", position_or_none, ("", ""), 0)
add("E32", position_or_none, ("", "a"), None)
add("E32", position_or_none, ("abc", "abc"), 0)
add("E32", position_or_none, ("abcabc", "bc"), 1)
add("E32", position_or_none, ("😀a", "a"), 1)

# E33
add("E33", format_receipt, ("чай", 42.5), "чай       |   42.50")
add("E33", format_receipt, ("кофе", 1234.5), "кофе      | 1234.50")
add("E33", format_receipt, ("", 0), "          |    0.00")
add("E33", format_receipt, ("очень длинное имя", 1), "очень длинное имя|    1.00")
add("E33", format_receipt, ("x", -1.5), "x         |   -1.50")

# E34
add("E34", words_to_dashes, ("  один\tдва  ",), "один-два")
add("E34", words_to_dashes, ("a  b",), "a-b")
add("E34", words_to_dashes, ("",), "")
add("E34", words_to_dashes, ("   ",), "")
add("E34", words_to_dashes, ("a\nb\tc",), "a-b-c")
add("E34", words_to_dashes, ("a",), "a")
add("E34", words_to_dashes, (" a ",), "a")

# E35
add("E35", parse_pairs, ("name=Alice; age=30",), "name:Alice | age:30")
add("E35", parse_pairs, ("  a = 1 ; b= 2  ",), "a:1 | b:2")
add("E35", parse_pairs, ("url=http://x",), "url:http://x")
add("E35", parse_pairs, ("",), "")
add("E35", parse_pairs, (" ; ; ",), "")
add("E35", parse_pairs, ("a=1; broken; c=3",), "ERROR")
add("E35", parse_pairs, ("a=",), "ERROR")
add("E35", parse_pairs, (":1",), "ERROR")
add("E35", parse_pairs, ("a=1;;b=2",), "a:1 | b:2")
add("E35", parse_pairs, ("a:1;b:2",), "ERROR")
add("E35", parse_pairs, ("a=b=c",), "a:b=c")
add("E35", parse_pairs, ("key = value with spaces",), "key:value with spaces")
add("E35", parse_pairs, ("=x",), "ERROR")

# E36
add("E36", initials, ("Ира Петрова",), "И.П")
add("E36", initials, ("  andrei   ivanov ",), "A.I")
add("E36", initials, ("mary-jane watson",), "M.W")
add("E36", initials, ("",), "")
add("E36", initials, ("   ",), "")
add("E36", initials, ("кот",), "К")
add("E36", initials, ("e\u0301 x",), "E.X")
add("E36", initials, ("😀 кот",), "😀.К")

# E37
add("E37", reformat_records, ("name: Alice ; age: 30; city: Moscow",), "name=Alice | age=30 | city=Moscow")
add("E37", reformat_records, ("a:1;b:2",), "a=1 | b=2")
add("E37", reformat_records, ("url: http://x",), "url=http://x")
add("E37", reformat_records, ("",), "")
add("E37", reformat_records, (" ; ; ",), "")
add("E37", reformat_records, ("a=1;b=2",), "ERROR")
add("E37", reformat_records, ("a:1; broken; c:3",), "ERROR")
add("E37", reformat_records, ("a:",), "ERROR")
add("E37", reformat_records, (":1",), "ERROR")
add("E37", reformat_records, ("a:1;;b:2",), "a=1 | b=2")
add("E37", reformat_records, ("a: x : y",), "a=x : y")
add("E37", reformat_records, (" a : 1 ",), "a=1")

# E38
add("E38", parse_tags, (" a  b ",), "a,b")
add("E38", parse_tags, ("a",), "a")
add("E38", parse_tags, ("",), "")
add("E38", parse_tags, ("   ",), "")
add("E38", parse_tags, ("a\tb\nc",), "a,b,c")
add("E38", parse_tags, ("a,b",), "a,b")
add("E38", parse_tags, ("a b  c",), "a,b,c")

# E39
add("E39", round_trip, ("A",), "A|1|1")
add("E39", round_trip, ("Я",), "Я|1|2")
add("E39", round_trip, ("😀",), "😀|1|4")
add("E39", round_trip, ("AЯ😀",), "AЯ😀|3|7")
add("E39", round_trip, ("",), "|0|0")
add("E39", round_trip, ("ß",), "ß|1|2")
add("E39", round_trip, ("é",), "é|1|2")
add("E39", round_trip, ("漢",), "漢|1|3")

# E40
add("E40", byte_or_char, ("A",), "char=A;byte=65")
add("E40", byte_or_char, ("Я",), "char=Я;byte=208")
add("E40", byte_or_char, ("😀",), "char=😀;byte=240")
add("E40", byte_or_char, ("",), "empty")
add("E40", byte_or_char, ("é",), "char=é;byte=195")

# E41
add("E41", width_counts, ("AЯ😀",), "1:1,2:1,3:0,4:1")
add("E41", width_counts, ("é",), "1:0,2:1,3:0,4:0")
add("E41", width_counts, ("",), "1:0,2:0,3:0,4:0")
add("E41", width_counts, ("e\u0301",), "1:1,2:1,3:0,4:0")
add("E41", width_counts, ("漢",), "1:0,2:0,3:1,4:0")
add("E41", width_counts, ("ß",), "1:0,2:1,3:0,4:0")
add("E41", width_counts, ("A",), "1:1,2:0,3:0,4:0")
add("E41", width_counts, ("😀😀",), "1:0,2:0,3:0,4:2")

# E42
add("E42", ascii_safe, ("ABC",), "same:ABC")
add("E42", ascii_safe, ("AЯ",), "lost:A?")
add("E42", ascii_safe, ("😀",), "lost:?")
add("E42", ascii_safe, ("",), "same:")
add("E42", ascii_safe, ("?",), "same:?")
add("E42", ascii_safe, ("A B",), "same:A B")
add("E42", ascii_safe, ("ß",), "lost:?")
add("E42", ascii_safe, ("é",), "lost:?")

# E43
add("E43", ascii_guard, (b"ABC",), "ok:ABC")
add("E43", ascii_guard, (b"A\xffB",), "bad:1:255")
add("E43", ascii_guard, (b"",), "ok:")
add("E43", ascii_guard, (b"\x80",), "bad:0:128")
add("E43", ascii_guard, (b"\x7f",), "ok:\x7f")
add("E43", ascii_guard, (b"\xd0\xaf",), "bad:0:208")
add("E43", ascii_guard, (b"~",), "ok:~")
add("E43", ascii_guard, (b"\x00",), "ok:\x00")
add("E43", ascii_guard, (b"A B",), "ok:A B")
add("E43", ascii_guard, (b"\xff",), "bad:0:255")

# E44
add("E44", fit_message, ("AЯ😀", 7), "AЯ😀|3|7")
add("E44", fit_message, ("AЯ😀", 6), "AЯ|2|3")
add("E44", fit_message, ("AЯ😀", 5), "AЯ|2|3")
add("E44", fit_message, ("AЯ😀", 4), "AЯ|2|3")
add("E44", fit_message, ("AЯ😀", 3), "AЯ|2|3")
add("E44", fit_message, ("AЯ😀", 2), "A|1|1")
add("E44", fit_message, ("AЯ😀", 1), "A|1|1")
add("E44", fit_message, ("AЯ😀", 0), "|0|0")
add("E44", fit_message, ("😀", 3), "|0|0")
add("E44", fit_message, ("😀", 4), "😀|1|4")
add("E44", fit_message, ("", 10), "|0|0")
add("E44", fit_message, ("A", 0), "|0|0")
add("E44", fit_message, ("A", 1), "A|1|1")
add("E44", fit_message, ("Я", 2), "Я|1|2")
add("E44", fit_message, ("Я", 1), "|0|0")
add("E44", fit_message, ("AЯ", 3), "AЯ|2|3")


def check_result(task, args, result, expected):
    if isinstance(expected, bool):
        if type(result) is not bool or result is not expected:
            raise AssertionError(f"{task}{args}: ожидался bool {expected!r}, получено {result!r}")
    elif expected is None:
        if result is not None:
            raise AssertionError(f"{task}{args}: ожидался None, получено {result!r}")
    elif isinstance(expected, int):
        if type(result) is not int or result != expected:
            raise AssertionError(f"{task}{args}: ожидалось int {expected!r}, получено {result!r}")
    elif isinstance(expected, str):
        if type(result) is not str or result != expected:
            raise AssertionError(f"{task}{args}: ожидалась строка {expected!r}, получено {result!r}")
    else:
        if result != expected:
            raise AssertionError(f"{task}{args}: ожидалось {expected!r}, получено {result!r}")


def run_table():
    for task, function, args, expected in CASES:
        check_result(task, args, function(*args), expected)


def run_palindrome_oracle():
    samples = [
        "", "a", "ab", "aba", "abba", "abcba", "abca", "шалаш", "абба",
        "Абба", "e\u0301", "😀", "😀a😀", "abca", "aaaa",
    ]
    for text in samples:
        expected = text == text[::-1]
        result = is_palindrome(text)
        if type(result) is not bool or result is not expected:
            raise AssertionError(f"E17 oracle {text!r}: ожидался {expected!r}, получено {result!r}")


def run_slice_oracle():
    samples = ["", "a", "ab", "abc", "abcdef", "Кот", "e\u0301x", "😀ab"]
    bounds = [None, -9, -5, -3, -2, -1, 0, 1, 2, 3, 5, 9]
    steps = [None, 1, 2, 3, -1, -2, -3]
    checked = 0
    for text in samples:
        for start in bounds:
            for stop in bounds:
                for step in steps:
                    expected = text[start:stop:step]
                    result = slice_like(text, start, stop, step)
                    check_result("E25 oracle", (text, start, stop, step), result, expected)
                    checked += 1
    for text in samples:
        for start in [None, -1, 0, 1]:
            for stop in [None, -1, 0, 1]:
                result = slice_like(text, start, stop, 0)
                check_result("E25 oracle step=0", (text, start, stop, 0), result, None)
                checked += 1
    return checked


def run_count_oracle():
    samples = ["", "a", "aa", "aaa", "aaaa", "абракадабра", "abababa", "😀😀😀"]
    subs = ["a", "aa", "бра", "aba", "😀", "😀😀"]
    checked = 0
    for text in samples:
        for sub in subs:
            expected = text.count(sub)
            result = manual_count(text, sub)
            check_result("E29 oracle", (text, sub), result, expected)
            checked += 1
    return checked


def run_replace_oracle():
    samples = [
        ("", "a", "b", -1),
        ("aaaa", "aa", "b", -1),
        ("aaaa", "aa", "b", 0),
        ("aaaa", "aa", "b", 1),
        ("aaaa", "aa", "b", 2),
        ("aaaa", "aa", "b", 10),
        ("abc", "b", "", -1),
        ("abc", "abc", "X", 1),
        ("banana", "na", "NA", 2),
        ("aaaa", "a", "aa", 2),
        ("Кот и кот", "кот", "***", -1),
        ("😀😀😀", "😀😀", "!", 1),
    ]
    checked = 0
    for text, old, new, limit in samples:
        expected = text.replace(old, new, limit)
        result = replace_limited(text, old, new, limit)
        check_result("E31 oracle", (text, old, new, limit), result, expected)
        checked += 1
    return checked


def main():
    task_ids = {task for task, *_ in CASES}
    expected_tasks = {f"E{number}" for number in range(15, 45)}
    missing = expected_tasks - task_ids
    if missing:
        raise AssertionError(f"Нет тестовых случаев для задач: {sorted(missing)}")

    run_table()
    oracle_count = run_slice_oracle()
    oracle_count += run_count_oracle()
    oracle_count += run_replace_oracle()
    run_palindrome_oracle()

    total = len(CASES) + oracle_count
    print(f"OK: {total} проверок, {len(task_ids)} задач (E15–E44)")
    print(f"    документированных случаев: {len(CASES)}")
    print(f"    оракульных сверок: {oracle_count}")


if __name__ == "__main__":
    main()
