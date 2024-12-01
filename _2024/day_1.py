from utils import read


def diff(A, B):
    return sum(abs(a - b) for a, b in zip(sorted(A), sorted(B)))


def similarity(A, B):
    return sum(a * B.count(a) for a in sorted(A) if a in B)


if __name__ == "__main__":
    A, B = read()
    print(f"difference: {diff(A, B)}")
    print(f"similarity: {similarity(A, B)}")
