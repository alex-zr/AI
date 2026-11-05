#!/usr/bin/env python3
"""Проверка структуры L01.

Материал преподавателя. Запуск:
    python3 check_structure.py <путь-к-рабочей-копии>

Скрипт проверяет дерево, обязательные файлы, .gitignore, чистоту рабочего
дерева и сообщение первого коммита. Он не проверяет качество журнала и
решения участника — это делает преподаватель по рубрике.
"""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED_FILE = HERE / "expected_tree.txt"
EXPECTED_COMMIT = "L01: scaffold module 1"
REQUIRED_IGNORE = {"__pycache__/", "*.pyc", ".DS_Store"}


def load_expected():
    lines = EXPECTED_FILE.read_text(encoding="utf-8").splitlines()
    return {line.strip() for line in lines if line.strip() and not line.startswith("#")}


def git(target, *args):
    return subprocess.run(
        ["git", "-C", str(target), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def main():
    if len(sys.argv) != 2:
        print("Использование: python3 check_structure.py <путь-к-рабочей-копии>")
        return 2

    target = Path(sys.argv[1]).resolve()
    expected = load_expected()
    failures = []
    notes = []

    if not target.is_dir():
        print(f"FAIL: папка не найдена: {target}")
        return 1

    actual = set()
    for path in target.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(target)
        if rel.parts and rel.parts[0] == ".git":
            continue
        actual.add(rel.as_posix())

    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        failures.append("нет файлов: " + ", ".join(missing))
    if extra:
        failures.append("лишние файлы: " + ", ".join(extra))

    for rel in ["README.md", "notes/permissions.md", "notes/session-log.md"]:
        path = target / rel
        if path.is_file() and path.stat().st_size == 0:
            failures.append(f"пустой обязательный файл: {rel}")

    gitignore = target / ".gitignore"
    if gitignore.is_file():
        lines = {
            line.strip()
            for line in gitignore.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        missing_ignore = REQUIRED_IGNORE - lines
        if missing_ignore:
            failures.append(
                ".gitignore не содержит: " + ", ".join(sorted(missing_ignore))
            )

    inside = git(target, "rev-parse", "--is-inside-work-tree")
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        failures.append("папка не является Git-репозиторием")
    else:
        status = git(target, "status", "--porcelain")
        if status.returncode != 0:
            failures.append("git status завершился ошибкой")
        elif status.stdout.strip():
            failures.append("рабочее дерево не чистое: " + status.stdout.strip().replace("\n", "; "))

        log = git(target, "log", "-1", "--pretty=%s")
        if log.returncode != 0:
            failures.append("коммит не найден")
        else:
            subject = log.stdout.strip()
            notes.append(f"коммит: {subject!r}")
            if subject != EXPECTED_COMMIT:
                failures.append(
                    f"сообщение коммита {subject!r}, ожидалось {EXPECTED_COMMIT!r}"
                )

        count = git(target, "rev-list", "--count", "HEAD")
        if count.returncode == 0:
            notes.append(f"коммитов: {count.stdout.strip()}")

        tracked = git(target, "ls-files")
        if tracked.returncode == 0:
            tracked_set = {
                line.strip() for line in tracked.stdout.splitlines() if line.strip()
            }
            untracked_expected = sorted(expected - tracked_set)
            if untracked_expected:
                failures.append(
                    "не добавлены в Git: " + ", ".join(untracked_expected)
                )

    print(f"Проверка: {target}")
    for note in notes:
        print(f"  {note}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("PASS: структура, коммит и чистота рабочего дерева соответствуют L01.")
    print("Не проверено скриптом: журнал разрешений и объяснение участника.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
