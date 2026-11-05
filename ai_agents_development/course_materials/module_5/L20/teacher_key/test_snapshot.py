"""Проверка шести демонстраций в резервном снимке L20."""

import subprocess
import sys
import unittest
from pathlib import Path


SNAPSHOT = Path(__file__).resolve().parent.parent / "snapshot"
EXPECTED = {
    "variables/example_1.py": "север\n",
    "variables/example_2.py": "юг\n",
    "conditions/example_1.py": "мало\n",
    "conditions/example_2.py": "достаточно\n",
    "loops/example_1.py": "шаг\nшаг\nшаг\n",
    "loops/example_2.py": "",
}


class SnapshotTests(unittest.TestCase):
    def test_demo_outputs(self):
        for path, expected in EXPECTED.items():
            with self.subTest(path=path):
                output = subprocess.check_output(
                    [sys.executable, "-B", str(SNAPSHOT / path)],
                    encoding="utf-8",
                    timeout=5,
                )
                self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
