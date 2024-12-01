import unittest


def read(filename="input"):
    A = []
    B = []

    with open(filename, "r") as file:
        for line in file:
            a, b = map(int, line.strip().split())
            A.append(a)
            B.append(b)

    return A, B
