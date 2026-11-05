"""Демонстрационные тесты L03. Материал преподавателя."""

import unittest

from shout import shout


class ShoutTest(unittest.TestCase):
    def test_lowercase(self):
        self.assertEqual(shout("ada"), "ADA!")

    def test_already_uppercase(self):
        self.assertEqual(shout("ADA"), "ADA!")


if __name__ == "__main__":
    unittest.main()
