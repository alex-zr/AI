"""Проверка двух входов для функции greet.

Это не unittest: формальные тесты вводятся на L03.
"""

from greet import greet

CASES = [
    ("Ada", "Привет, Ada!"),
    ("Борис", "Привет, Борис!"),
]


def main():
    failures = 0
    for name, expected in CASES:
        print(f"Вход: {name!r}")
        print(f"Ожидалось: {expected!r}")
        try:
            actual = greet(name)
        except Exception as exc:  # показываем ошибку, а не скрываем её
            print(f"Фактически: ошибка {type(exc).__name__}: {exc}")
            failures += 1
            continue

        print(f"Фактически: {actual!r}")
        if actual != expected:
            failures += 1

    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
