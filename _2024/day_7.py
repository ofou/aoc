from itertools import product


def read_map(filename):
    with open(filename) as f:
        lines = [line.rstrip("\n") for line in f if line.strip()]
    return lines


def parse_data(lines):
    equations = []
    for line in lines:
        left, right = line.split(":")
        test_value = int(left.strip())
        values = list(map(int, right.strip().split()))
        equations.append((test_value, values))
    return equations


def apply_op(current, val, op):
    if op == "+":
        return current + val
    elif op == "*":
        return current * val
    else:  # op == '||'
        return int(str(current) + str(val))


def can_solve_equation(result, values):
    if len(values) == 1:
        return values[0] == result

    operators = ["+", "*", "||"]
    n = len(values)
    for ops in product(operators, repeat=n - 1):
        current = values[0]
        valid = True
        for op, val in zip(ops, values[1:]):
            current = apply_op(current, val, op)
        if current == result:
            return True
    return False


if __name__ == "__main__":
    data = read_map("data/7")
    equations = parse_data(data)

    total = 0
    for result, values in equations:
        if can_solve_equation(result, values):
            total += result

    print(total)
