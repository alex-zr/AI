"""Независимая проверка требований L04. Материал преподавателя."""

import unittest

from greet import greet


class L04AcceptanceTest(unittest.TestCase):
    def test_default_plain_name(self):
        self.assertEqual(greet("Ada"), "Привет, Ada!")

    def test_default_surrounding_spaces(self):
        self.assertEqual(greet("  Ada  "), "Привет, Ada!")

    def test_default_inner_space(self):
        self.assertEqual(greet("Ada Lovelace"), "Привет, Ada Lovelace!")

    def test_custom_greeting(self):
        self.assertEqual(greet("Ada", "Здравствуйте"), "Здравствуйте, Ada!")

    def test_custom_greeting_with_spaces(self):
        self.assertEqual(greet("  Ada  ", "Здравствуйте"), "Здравствуйте, Ada!")


if __name__ == "__main__":
    unittest.main()
