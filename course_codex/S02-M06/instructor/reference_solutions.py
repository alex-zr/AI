"""Эталонные решения S02-M06 — только для преподавателя.

Не выдавать ученикам до самостоятельной попытки.
Целевая версия: Python 3.14; проверено на CPython 3.14.8.
"""


def edge_report(text):
    if not text:
        return "0|-|-"
    return f"{len(text)}|{text[0]}|{text[-1]}"


def codepoint_label(ch):
    if len(ch) != 1:
        return "invalid"
    return f"{ch}={hex(ord(ch))}"


def is_palindrome(text):
    left = 0
    right = len(text) - 1
    while left < right:
        if text[left] != text[right]:
            return False
        left += 1
        right -= 1
    return True


def char_at(text, index):
    if -len(text) <= index < len(text):
        return f"ok:{text[index]}"
    return "missing"


def shift_letters(text, shift):
    shift = shift % 26
    result = ""
    for ch in text:
        code = ord(ch)
        if 65 <= code <= 90:
            code = 65 + (code - 65 + shift) % 26
            result += chr(code)
        else:
            result += ch
    return result


def last_char(text):
    if not text:
        return ""
    return text[-1]


def reverse_and_skip(text):
    return f"{text[::-1]}|{text[::2]}"


def mask_card(number):
    if len(number) < 8:
        return "*" * len(number)
    return number[:4] + "*" * (len(number) - 8) + number[-4:]


def rotate(text, k):
    if not text:
        return ""
    k = k % len(text)
    return text[k:] + text[:k]


def trim_around(text, left, right):
    keep = len(text) - left - right
    if keep <= 0:
        return ""
    return text[left:left + keep]


def slice_like(text, start=None, stop=None, step=None):
    n = len(text)
    if step is None:
        step = 1
    if step == 0:
        return None

    if step > 0:
        lower = 0
        upper = n
    else:
        lower = -1
        upper = n - 1

    if start is None:
        start = lower if step > 0 else upper
    else:
        if start < 0:
            start += n
        if start < lower:
            start = lower
        if start > upper:
            start = upper

    if stop is None:
        stop = upper if step > 0 else lower
    else:
        if stop < 0:
            stop += n
        if stop < lower:
            stop = lower
        if stop > upper:
            stop = upper

    result = ""
    index = start
    if step > 0:
        while index < stop:
            result += text[index]
            index += step
    else:
        while index > stop:
            result += text[index]
            index += step
    return result


def drop_last(text):
    if not text:
        return ""
    return text[:-1]


def censor(text, word):
    return text.replace(word, "*" * len(word))


def has_extension(name, ext):
    return name.endswith(ext)


def manual_count(text, sub):
    count = 0
    start = 0
    while True:
        position = text.find(sub, start)
        if position == -1:
            return count
        count += 1
        start = position + len(sub)


def normalize_and_mark(text):
    text = text.strip()
    if text.endswith("!"):
        text = text[:-1]
    return text


def replace_limited(text, old, new, limit):
    if limit == 0:
        return text
    result = ""
    start = 0
    replaced = 0
    while limit < 0 or replaced < limit:
        position = text.find(old, start)
        if position == -1:
            break
        result += text[start:position] + new
        start = position + len(old)
        replaced += 1
    return result + text[start:]


def position_or_none(text, sub):
    position = text.find(sub)
    if position == -1:
        return None
    return position


def format_receipt(name, price):
    return f"{name:<10}|{price:>8.2f}"


def words_to_dashes(text):
    return "-".join(text.split())


def parse_pairs(text):
    result = ""
    for chunk in text.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        position = chunk.find("=")
        if position <= 0:
            return "ERROR"
        key = chunk[:position].strip()
        value = chunk[position + 1:].strip()
        if not key or not value:
            return "ERROR"
        if result:
            result += " | "
        result += f"{key}:{value}"
    return result


def initials(full_name):
    result = ""
    for part in full_name.split():
        if result:
            result += "."
        result += part[0].upper()
    return result


def reformat_records(text):
    result = ""
    for record in text.split(";"):
        record = record.strip()
        if not record:
            continue
        position = record.find(":")
        if position <= 0:
            return "ERROR"
        key = record[:position].strip()
        value = record[position + 1:].strip()
        if not key or not value:
            return "ERROR"
        if result:
            result += " | "
        result += f"{key}={value}"
    return result


def parse_tags(line):
    return ",".join(line.split())


def round_trip(text):
    data = text.encode("utf-8")
    return f"{text}|{len(text)}|{len(data)}"


def byte_or_char(text):
    if not text:
        return "empty"
    data = text.encode("utf-8")
    return f"char={text[0]};byte={data[0]}"


def width_counts(text):
    one = 0
    two = 0
    three = 0
    four = 0
    for ch in text:
        size = len(ch.encode("utf-8"))
        if size == 1:
            one += 1
        elif size == 2:
            two += 1
        elif size == 3:
            three += 1
        else:
            four += 1
    return f"1:{one},2:{two},3:{three},4:{four}"


def ascii_safe(text):
    data = text.encode("ascii", errors="replace")
    safe = data.decode("ascii")
    if safe == text:
        return f"same:{safe}"
    return f"lost:{safe}"


def ascii_guard(data):
    result = ""
    for index in range(len(data)):
        value = data[index]
        if value > 127:
            return f"bad:{index}:{value}"
        result += chr(value)
    return "ok:" + result


def fit_message(text, limit):
    used = 0
    count = 0
    for ch in text:
        size = len(ch.encode("utf-8"))
        if used + size > limit:
            break
        used += size
        count += 1
    prefix = text[:count]
    return f"{prefix}|{len(prefix)}|{used}"
