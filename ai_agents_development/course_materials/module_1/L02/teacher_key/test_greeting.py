"""Проверка эталона L02. Материал преподавателя.

Не выдавать до L03: формальные тесты вводятся на следующем занятии.
"""

import unittest

from greet import greet


class GreetTest(unittest.TestCase):
    def test_ada(self):
        self.assertEqual(greet("Ada"), "Привет, Ada!")

    def test_boris(self):
        self.assertEqual(greet("Борис"), "Привет, Борис!")

    def test_oral_check(self):
        self.assertEqual(greet("Виктор"), "Привет, Виктор!")


if __name__ == "__main__":
    unittest.main()
