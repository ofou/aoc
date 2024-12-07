def check_word(grid, word, i, j, dx, dy, rows, cols):
    return (
        all(0 <= i + dx * k < rows and 0 <= j + dy * k < cols for k in range(len(word)))
        and "".join(grid[i + dx * k][j + dy * k] for k in range(len(word))) == word
    )


def count_words(grid, word):
    """
    >>> data = read("data/4")
    >>> word = 'XMAS'
    >>> count_words(data, word)
    2336
    """
    rows, cols = len(grid), len(grid[0])
    count = 0
    for i in range(rows):
        for j in range(cols):
            for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                if check_word(grid, word, i, j, dx, dy, rows, cols) or check_word(
                    grid, word[::-1], i, j, dx, dy, rows, cols
                ):
                    count += 1
    return count


def read(input):
    if isinstance(input, str):
        with open(input, "r") as file:
            content = file.read()
    elif isinstance(input, bytes):
        content = input.decode("utf-8")
    else:
        content = input if isinstance(input, str) else "".join(input)

    return [list(line) for line in content.splitlines()]


def rotate_grid(grid):
    return [list(row) for row in zip(*grid[::-1])]


def check_base_x_mas(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0
    for i in range(rows - 2):
        for j in range(cols - 2):
            # Check for 'MAS' going diagonally up-right from (i, j)
            if (
                "".join(grid[i + k][j + k] for k in range(3)) == "MAS"
                and "".join(grid[i + k][j + 2 - k] for k in range(3)) == "MAS"
            ):
                count += 1
    return count


def count_x_mas_rotational(grid):
    """Count X-mas patterns where A is center with M,M,S,S in diagonals.

    >>> data = read("data/4")
    >>> count_x_mas_rotational(data)
    1831
    """
    rows, cols = len(grid), len(grid[0])
    count = 0

    # Valid patterns in clockwise order from top-right
    valid_patterns = {"MMSS", "SMMS", "SSMM", "MSSM"}

    # Check inner grid points
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if grid[i][j] != "A":
                continue

            # Get diagonals clockwise from top-right
            diagonals = (
                grid[i - 1][j + 1],  # top-right
                grid[i + 1][j + 1],  # bottom-right
                grid[i + 1][j - 1],  # bottom-left
                grid[i - 1][j - 1],  # top-left
            )

            if "".join(diagonals) in valid_patterns:
                count += 1

    return count


if __name__ == "__main__":
    data = read("data/4")
    count = count_x_mas_rotational(data)
    print(f"Total X-MAS count: {count}")
