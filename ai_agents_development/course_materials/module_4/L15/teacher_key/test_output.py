"""Закрытая проверка вывода примера в переданной учебной копии."""

import subprocess
import sys
import unittest
from pathlib import Path


class HandoffOutputTests(unittest.TestCase):
    def test_example_preserves_the_final_value(self):
        output = subprocess.check_output(
            [sys.executable, "-B", "example.py"],
            cwd=EXAMPLE_DIR,
            encoding="utf-8",
            timeout=5,
        )
        self.assertEqual(output, "вечер\n")


if __name__ == "__main__":
    EXAMPLE_DIR = Path(sys.argv.pop(1)).resolve()
    unittest.main()
