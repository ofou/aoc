def read(input):
    lines = (
        open(input).read().splitlines()
        if isinstance(input, str)
        else input.decode("utf-8").splitlines()
    )

    return [[int(x) for x in line.split()] for line in lines]


def report(case):
    r"""
    >>> data = "7 6 4 2 1\n1 2 7 8 9\n9 7 6 2 1\n1 3 2 4\n8 6 4 4 1\n1 3 6 7 9".encode('utf-8')
    >>> data = read(data)
    >>> sum(report(case) for case in data)
    2

    >>> data = read("data/2")
    >>> sum(report(case) for case in data)
    224
    """

    diffs = [b - a for a, b in zip(case, case[1:])]  # pairwise(case)
    return int(
        diffs and all(1 <= abs(d) <= 3 for d in diffs) and min(diffs) * max(diffs) > 0
    )


def dampener(case):
    r"""
    >>> data = "7 6 4 2 1\n1 2 7 8 9\n9 7 6 2 1\n1 3 2 4\n8 6 4 4 1\n1 3 6 7 9".encode('utf-8')
    >>> data = read(data)
    >>> sum(any(report(problem) for problem in dampener(case)) for case in data)
    4

    >>> data = read("data/2")
    >>> sum(any(report(problem) for problem in dampener(case)) for case in data)
    293

    """
    return [case[:i] + case[i + 1 :] for i in range(len(case))]


if __name__ == "__main__":
    data = read("data/2")
    reports = sum(report(case) for case in data)
    print(f"Part One: {reports}")

    dampened = sum(any(report(problem) for problem in dampener(case)) for case in data)
    print(f"Part Two: {dampened}")
