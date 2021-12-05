import re
from collections import defaultdict

from util import *

DAY = 5
YEAR = 2021


def parse_line(line):
    m = re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line)
    return [*map(int, m.groups())]


def sign(a: int):
    return (a > 0) - (a < 0)


def solve(lines, diagonals=False):
    count = defaultdict(lambda: 0)
    for line in lines:
        x1, y1, x2, y2 = line
        if not diagonals and not (x1 == x2 or y1 == y2):
            continue

        dx, dy = sign(x2 - x1), sign(y2 - y1)
        x, y = x1, y1
        count[(x, y)] += 1
        while (x, y) != (x2, y2):
            x, y = x + dx, y + dy
            count[(x, y)] += 1
    return sum(i > 1 for i in count.values())


def part1(lines):
    return solve(lines)


def part2(lines):
    return solve(lines, diagonals=True)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True).split("\n")
    lines = [*map(parse_line, data)]
    res = part1(lines)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(lines)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
