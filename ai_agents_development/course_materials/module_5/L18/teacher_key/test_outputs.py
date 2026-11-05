"""Проверка вывода демонстраций и эталона на известных входах."""

import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


class OutputTests(unittest.TestCase):
    def test_cases(self):
        cases = (
            ("demo.py", 9, "ожидание\n"),
            ("demo.py", 10, "доступ\n"),
            ("demo_bad.py", 9, "ожидание\n"),
            ("demo_bad.py", 10, "ожидание\n"),
            ("reference.py", 4, "мало\n"),
            ("reference.py", 5, "достаточно\n"),
        )
        for filename, value, expected in cases:
            with self.subTest(filename=filename, value=value):
                first, rest = Path(__file__).with_name(filename).read_text(
                    encoding="utf-8"
                ).split("\n", 1)
                self.assertTrue(first.startswith("amount = "))
                with TemporaryDirectory() as folder:
                    script = Path(folder) / filename
                    script.write_text(f"amount = {value}\n{rest}", encoding="utf-8")
                    result = subprocess.check_output(
                        [sys.executable, "-B", str(script)], encoding="utf-8", timeout=5
                    )
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
