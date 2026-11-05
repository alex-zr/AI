"""Проверка мини-примера на двух входах, отдельно от проверяемой копии."""

import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


class OutputTests(unittest.TestCase):
    def check_output_for(self, amount, expected):
        first_line, body = SOURCE.read_text(encoding="utf-8").split("\n", 1)
        self.assertEqual(first_line, "amount = 5", "Изменено исходное значение")
        with TemporaryDirectory() as directory:
            script = Path(directory) / "example.py"
            script.write_text(f"amount = {amount}\n{body}", encoding="utf-8")
            actual = subprocess.check_output(
                [sys.executable, "-B", str(script)], encoding="utf-8", timeout=5
            )
        self.assertEqual(actual, expected, f"Неверный вывод при amount={amount}")

    def test_below_threshold(self):
        self.check_output_for(4, "мало\n")

    def test_at_threshold(self):
        self.check_output_for(5, "достаточно\n")


if __name__ == "__main__":
    SOURCE = Path(sys.argv.pop(1)).resolve()
    unittest.main()
