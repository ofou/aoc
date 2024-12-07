def read_map(filename):
    with open(filename) as f:
        lines = [line.rstrip("\n") for line in f]
    return lines


def turn_right(direction):
    dirs = ["^", ">", "v", "<"]
    return dirs[(dirs.index(direction) + 1) % 4]


def forward_position(x, y, direction):
    if direction == "^":
        return x - 1, y
    elif direction == "v":
        return x + 1, y
    elif direction == "<":
        return x, y - 1
    elif direction == ">":
        return x, y + 1


def find_guard(grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell in "^v<>":
                return i, j, cell
    return None, None, None


def simulate_guard_with_obstacle(grid, obstacle_pos=None):
    """
    Simulate the guard's movement.
    If obstacle_pos is given (x, y), place '#' there temporarily.
    Detect if the guard falls into a loop.
    Return:
       - "left" if guard leaves the map,
       - "loop" if guard gets stuck in a loop.
    """
    rows = len(grid)
    cols = len(grid[0])
    # Convert to a mutable grid
    grid_list = [list(row) for row in grid]

    # Find guard initial state
    gx, gy, direction = find_guard(grid)
    # Replace guard symbol with '.' in the grid since we track guard separately
    grid_list[gx][gy] = "."

    # Place the temporary obstacle if given
    if obstacle_pos is not None:
        ox, oy = obstacle_pos
        original = grid_list[ox][oy]
        grid_list[ox][oy] = "#"
    else:
        original = None

    visited_states = set()
    visited_states.add((gx, gy, direction))

    while True:
        nx, ny = forward_position(gx, gy, direction)

        # If out of bounds
        if nx < 0 or nx >= rows or ny < 0 or ny >= cols:
            # Guard leaves the map
            result = "left"
            break

        # If there's an obstacle in front, turn right
        if grid_list[nx][ny] == "#":
            direction = turn_right(direction)
        else:
            # Move forward
            gx, gy = nx, ny
            # Check if we have a repeated state
            if (gx, gy, direction) in visited_states:
                # Loop detected
                result = "loop"
                break
            visited_states.add((gx, gy, direction))

    # Revert the obstacle placement if any
    if obstacle_pos is not None:
        ox, oy = obstacle_pos
        grid_list[ox][oy] = original

    return result


def count_loop_positions(grid):
    rows = len(grid)
    cols = len(grid[0])

    # Find guard initial position
    gx, gy, _ = find_guard(grid)

    loop_count = 0
    for x in range(rows):
        for y in range(cols):
            # Can't place where guard starts, can't place on existing obstacles
            if (x, y) == (gx, gy):
                continue
            if grid[x][y] != ".":
                continue

            outcome = simulate_guard_with_obstacle(grid, (x, y))
            if outcome == "loop":
                loop_count += 1

    return loop_count


if __name__ == "__main__":
    # Example usage:
    # Assuming 'input.txt' contains the puzzle input map
    grid = read_map("data/6")
    answer = count_loop_positions(grid)
    print(answer)
