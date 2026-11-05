"""Проверка вывода демонстраций и эталона на известных входах."""

import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


class OutputTests(unittest.TestCase):
    def test_cases(self):
        cases = (
            ("demo.py", 2, "точка\n" * 2),
            ("demo.py", 0, ""),
            ("demo_bad.py", 2, "точка\n" * 3),
            ("demo_bad.py", 0, "точка\n"),
            ("reference.py", 3, "шаг\n" * 3),
            ("reference.py", 0, ""),
        )
        for filename, value, expected in cases:
            with self.subTest(filename=filename, value=value):
                first, rest = Path(__file__).with_name(filename).read_text(
                    encoding="utf-8"
                ).split("\n", 1)
                self.assertTrue(first.startswith("n = "))
                with TemporaryDirectory() as folder:
                    script = Path(folder) / filename
                    script.write_text(f"n = {value}\n{rest}", encoding="utf-8")
                    result = subprocess.check_output(
                        [sys.executable, "-B", str(script)], encoding="utf-8", timeout=5
                    )
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
