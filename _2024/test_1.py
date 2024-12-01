import unittest
from utils import read
from _2024.day_1 import diff, similarity
import unittest


class part_1(unittest.TestCase):
    def test_toy(self):
        A, B = read("toy")
        self.assertEqual(diff(A, B), 11)

    def test_input(self):
        A, B = read("input")
        self.assertEqual(diff(A, B), 2264607)


class part_2(unittest.TestCase):
    def test_toy(self):
        A, B = read("toy")
        self.assertEqual(similarity(A, B), 31)

    def test_input(self):
        A, B = read("input")
        self.assertEqual(similarity(A, B), 19457120)


if __name__ == "__main__":
    unittest.main()
