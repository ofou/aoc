import re

def read(input):
    if isinstance(input, str):
        with open(input, 'r') as file:
            content = file.read()
    elif isinstance(input, bytes): 
        content = input.decode('utf-8')
    else:
        content = input if isinstance(input, str) else ''.join(input)

    pattern = r"(mul\(\d+,\d+\)|do\(\)|don't\(\))"
    matches = re.findall(pattern, content)

    return matches

def corrupt(case):
    r"""
    >>> data = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))".encode('utf-8')
    >>> corrupt(read(data))
    161

    >>> data = read("data/3")
    >>> matches = read(data)
    >>> corrupt(matches)
    183669043
    """
    sum = 0
    for c in case:
        if c.startswith("mul"):
            c = c.strip('mul()')
            a, b = c.split(',')
            sum += int(a) * int(b)

    return sum

def disabled(case):
    r"""
    >>> data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))".encode('utf-8')
    >>> disabled(read(data))
    48

    >>> data = read("data/3")
    >>> matches = read(data)
    >>> disabled(matches)
    59097164
    """
    sum = 0
    enabled = True
    for c in case:
        if c == "do()":
            enabled = True
        elif c == "don't()":
            enabled = False
        elif enabled and c.startswith("mul"):
            c = c.strip('mul()')
            a, b = c.split(',')
            sum += int(a) * int(b)
    return sum

if __name__ == "__main__":
    data = read("data/3")
    matches = read(data)
    
    # For Part One
    print(f"Part One: {corrupt(matches)}")
    
    # For Part Two
    print(f"Part Two: {disabled(matches)}")