import io
import unittest
from contextlib import redirect_stdout

from demo_examples import demo, reference


class OutputTests(unittest.TestCase):
    def test_demo_prints_the_value_of_animal(self):
        output = io.StringIO()
        with redirect_stdout(output):
            demo()
        self.assertEqual(output.getvalue(), "кот\n")

    def test_reference_prints_the_value_from_the_draft(self):
        output = io.StringIO()
        with redirect_stdout(output):
            reference()
        self.assertEqual(output.getvalue(), "Аня\n")


if __name__ == "__main__":
    unittest.main()
