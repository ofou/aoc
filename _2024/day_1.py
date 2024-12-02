def read(input):
    lines = (
        open(input).read().splitlines()
        if isinstance(input, str)
        else input.decode("utf-8").splitlines()
    )
    return zip(*(map(int, line.split()) for line in lines))


def diff(A, B):
    r"""
    >>> data = "3 4\n4 3\n2 5\n1 3\n3 9\n3 3".encode('utf-8')
    >>> A, B = read(data)
    >>> diff(A, B)
    11

    >>> A, B = read("data/1")
    >>> diff(A, B)
    2264607
    """
    return sum(abs(a - b) for a, b in zip(sorted(A), sorted(B)))


def similarity(A, B):
    r"""
    >>> data = "3 4\n4 3\n2 5\n1 3\n3 9\n3 3".encode('utf-8')
    >>> A, B = read(data)
    >>> similarity(A, B)
    31

    >>> A, B = read("data/1")
    >>> similarity(A, B)
    19457120
    """
    return sum(a * B.count(a) for a in sorted(A) if a in B)


if __name__ == "__main__":
    A, B = read("data/1")
    print(f"Part One: {diff(A, B)}")
    print(f"Part Two: {similarity(A, B)}")
