import unittest

from greet import greet


class GreetTest(unittest.TestCase):
    def test_plain_name(self):
        self.assertEqual(greet("Ada"), "Привет, Ada!")

    def test_surrounding_spaces(self):
        self.assertEqual(greet("  Ada  "), "Привет, Ada!")

    def test_inner_space(self):
        self.assertEqual(greet("Ada Lovelace"), "Привет, Ada Lovelace!")


if __name__ == "__main__":
    unittest.main()
