"""Проверка демонстрационного примера L02. Материал преподавателя."""

import unittest

from welcome import welcome


class WelcomeTest(unittest.TestCase):
    def test_moscow(self):
        self.assertEqual(welcome("Москва"), "Добро пожаловать в Москва!")

    def test_kazan(self):
        self.assertEqual(welcome("Казань"), "Добро пожаловать в Казань!")


if __name__ == "__main__":
    unittest.main()
