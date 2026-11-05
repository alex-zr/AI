#!/usr/bin/env python3
"""Проверка L03: тесты должны падать на baseline и проходить на решении.

Материал преподавателя. Запуск:
    python3 verify_l03.py <путь-к-рабочей-копии>

Проверяется:
- ровно три тестовых метода;
- тесты падают на исходном дефектном greet.py;
- тесты проходят на greet.py участника.
"""

import ast
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASELINE = HERE / "baseline" / "greet.py"


def count_tests(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
    ]


def run_tests(cwd):
    return subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-v",
        ],
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def tail(text, limit=25):
    lines = text.strip().splitlines()
    return "\n".join(lines[-limit:])


def main():
    if len(sys.argv) != 2:
        print("Использование: python3 verify_l03.py <путь-к-рабочей-копии>")
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

    names = count_tests(tests)
    print(f"Тестовых методов: {len(names)}")
    for name in names:
        print(f"  - {name}")
    if len(names) != 3:
        print("FAIL: по карточке L03 нужны ровно три теста.")
        return 1

    with tempfile.TemporaryDirectory(prefix="l03-check-") as tmp:
        work = Path(tmp)
        shutil.copytree(
            target / "tests",
            work / "tests",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        shutil.copyfile(BASELINE, work / "greet.py")

        baseline = run_tests(work)
        print("\n--- Baseline: ожидается падение ---")
        print(f"код возврата: {baseline.returncode}")
        print(tail(baseline.stdout + "\n" + baseline.stderr))
        if baseline.returncode == 0:
            print("FAIL: тесты проходят на дефектном baseline и не ловят дефект.")
            return 1
        if "skipped=" in (baseline.stdout + baseline.stderr).lower():
            print("FAIL: в запуске есть пропущенные тесты; поведение не проверено.")
            return 1

        shutil.copyfile(greet, work / "greet.py")
        fixed = run_tests(work)
        print("\n--- Решение: ожидается успех ---")
        print(f"код возврата: {fixed.returncode}")
        print(tail(fixed.stdout + "\n" + fixed.stderr))
        if fixed.returncode != 0:
            print("FAIL: тесты не проходят на решении участника.")
            return 1
        if "skipped=" in (fixed.stdout + fixed.stderr).lower():
            print("FAIL: в зелёном запуске есть пропущенные тесты.")
            return 1

    print("\nPASS: тесты падают на baseline и проходят на решении.")
    print("Не проверено скриптом: минимальность diff и отсутствие правок BEHAVIORS.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
