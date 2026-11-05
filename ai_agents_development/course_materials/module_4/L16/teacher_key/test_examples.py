"""Закрытая проверка демонстраций и эталона L16."""

import subprocess
import sys
import unittest
from pathlib import Path


class VariableOutputTests(unittest.TestCase):
    def test_expected_outputs(self):
        expected = {
            "demo_initial.py": "синий\n",
            "demo_replaced.py": "зелёный\n",
            "example.py": "вечер\n",
        }
        for script, output in expected.items():
            with self.subTest(script=script):
                result = subprocess.check_output(
                    [sys.executable, "-B", str(Path(__file__).with_name(script))],
                    encoding="utf-8",
                    timeout=5,
                )
                self.assertEqual(result, output)


if __name__ == "__main__":
    unittest.main()
