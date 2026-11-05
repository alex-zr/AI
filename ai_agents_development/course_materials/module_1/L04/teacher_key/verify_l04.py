#!/usr/bin/env python3
"""Проверка L04: старые и новые тесты плюс независимые требования.

Материал преподавателя. Запуск:
    python3 verify_l04.py <путь-к-выбранной-рабочей-копии>

Проверяется:
- три исходных теста сохранены;
- всего ровно пять тестов;
- тесты участника проходят;
- независимые acceptance-тесты проходят.
"""

import ast
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ACCEPTANCE = HERE / "acceptance_test.py"
OLD_TESTS = {
    "test_plain_name",
    "test_surrounding_spaces",
    "test_inner_space",
}


def test_names(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
    ]


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, check=False)


def tail(text, limit=25):
    lines = text.strip().splitlines()
    return "\n".join(lines[-limit:])


def main():
    if len(sys.argv) != 2:
        print("Использование: python3 verify_l04.py <путь-к-выбранной-рабочей-копии>")
        return 2

    target = Path(sys.argv[1]).resolve()
    greet = target / "greet.py"
    tests = target / "tests" / "test_greet.py"

    if not greet.is_file():
        print(f"FAIL: не найден {greet}")
        return 1
    if not tests.is_file():
        print(f"FAIL: не найден {tests}")
        return 1

    names = test_names(tests)
    print(f"Тестовых методов: {len(names)}")
    for name in names:
        print(f"  - {name}")

    missing_old = sorted(OLD_TESTS - set(names))
    if missing_old:
        print("FAIL: не найдены исходные тесты: " + ", ".join(missing_old))
        return 1
    if len(names) != 5:
        print("FAIL: по карточке L04 нужны три старых и ровно два новых теста.")
        return 1

    own = run(
        [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"],
        target,
    )
    print("\n--- Тесты участника: ожидается успех ---")
    print(f"код возврата: {own.returncode}")
    print(tail(own.stdout + "\n" + own.stderr))
    if own.returncode != 0:
        print("FAIL: тесты участника не проходят.")
        return 1
    if "skipped=" in (own.stdout + own.stderr).lower():
        print("FAIL: в тестах участника есть пропущенные проверки.")
        return 1

    with tempfile.TemporaryDirectory(prefix="l04-check-") as tmp:
        work = Path(tmp)
        shutil.copyfile(greet, work / "greet.py")
        shutil.copyfile(ACCEPTANCE, work / "test_acceptance.py")
        accepted = run(
            [sys.executable, "-B", "-m", "unittest", "-v", "test_acceptance.py"],
            work,
        )
        print("\n--- Независимые требования: ожидается успех ---")
        print(f"код возврата: {accepted.returncode}")
        print(tail(accepted.stdout + "\n" + accepted.stderr))
        if accepted.returncode != 0:
            print("FAIL: независимая проверка требований L04 не прошла.")
            return 1
        if "skipped=" in (accepted.stdout + accepted.stderr).lower():
            print("FAIL: в независимой проверке есть пропущенные тесты.")
            return 1

    print("\nPASS: старые и новые тесты проходят, независимые требования L04 выполнены.")
    print("Не проверено скриптом: одинаковый базовый коммит, порядок попыток и качество журнала.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
