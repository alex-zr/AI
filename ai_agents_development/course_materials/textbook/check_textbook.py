#!/usr/bin/env python3
"""Проверка структуры и ссылок учебника.

Скрипт не проверяет методическое качество и не запускает примеры.
Он отвечает только на вопросы: существует ли глава, есть ли обязательные
разделы, разрешаются ли относительные ссылки и нет ли ссылок на закрытые
материалы.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATERIALS = ROOT / "course_materials"
GUIDES = sorted(MATERIALS.glob("module_*/L*/student_guide.md"))
NEW_GUIDES = [guide for guide in GUIDES if guide.parent.name != "L01"]

REQUIRED = {
    "паспорт": "## Паспорт занятия",
    "зачем в проекте": "Зачем этот приём",
    "маршрут 75+75": "75",
    "теория": ("Теория", "Основные понятия"),
    "разобранные примеры": ("Разобранные примеры", "Разобранная демонстрация"),
    "схема mermaid": "```mermaid",
    "карточка практики": "practice_card.md",
    "самопроверка": "Самопроверка",
    "OpenCode": "OpenCode",
    "Codex": "Codex",
    "углубление": "Углубление",
    "вопросы": "Контрольные вопросы",
    "словарь": "Словарь",
    "переход": "Переход к следующему",
    "источники": "Источники",
}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
ANCHOR_RE = re.compile(r'<a\s+id="([^"]+)"')
CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")


def slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text)
    return text.strip("-")


def anchors(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    result = set(ANCHOR_RE.findall(text))
    for _, title in HEADING_RE.findall(text):
        result.add(slug(title))
    return result


def check_guide(path: Path, cache: dict[Path, set[str]], full: bool = True) -> list[str]:
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")
    label = str(path.relative_to(ROOT))

    for name, needle in (REQUIRED.items() if full else ()):
        needles = needle if isinstance(needle, tuple) else (needle,)
        if not any(item in text for item in needles):
            problems.append(f"{label}: нет обязательного признака «{name}»")

    if "teacher_key" in text:
        problems.append(f"{label}: упоминание закрытых материалов teacher_key")

    for raw in LINK_RE.findall(text):
        target = raw.strip()
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if target.startswith("#"):
            target_path, anchor = path, target[1:]
        else:
            target_path, _, anchor = target.partition("#")
            target_path = (path.parent / target_path).resolve()
            if not target_path.exists():
                problems.append(f"{label}: битая ссылка {raw}")
                continue
            if target_path.is_dir():
                continue
            anchor = anchor or ""

        if anchor:
            if target_path not in cache:
                cache[target_path] = anchors(target_path)
            if anchor not in cache[target_path]:
                problems.append(f"{label}: не найден якорь #{anchor} в {raw}")

    return problems


def main() -> int:
    all_problems: list[str] = []
    cache: dict[Path, set[str]] = {}

    print(f"Найдено руководств: {len(GUIDES)} (полная структурная проверка: L02–L24)")
    for guide in GUIDES:
        print(f"  {guide.relative_to(ROOT)}")
        all_problems.extend(check_guide(guide, cache, full=guide.parent.name != "L01"))

    expected = {f"L{number:02d}" for number in range(1, 25)}
    found = {guide.parent.name for guide in GUIDES}
    missing = sorted(expected - found)
    if missing:
        print(f"Нет руководств: {', '.join(missing)}")

    print(f"Проблем: {len(all_problems)}")
    for problem in all_problems:
        print(f"  - {problem}")
    return 1 if all_problems else 0


if __name__ == "__main__":
    sys.exit(main())
