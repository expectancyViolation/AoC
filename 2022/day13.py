import functools
from math import prod

from util import *

DAY = 13
YEAR = 2022


def compare_int(i1, i2):
    return (i2 < i1) - (i1 < i2)


def compare(p1, p2):
    i1, i2 = (isinstance(x, int) for x in (p1, p2))
    if i1 and i2:
        return compare_int(p1, p2)
    if i1:
        p1 = [p1]
    if i2:
        p2 = [p2]
    for a, b in zip(p1, p2):
        if c := compare(a, b):
            return c
    return compare_int(len(p1), len(p2))


def part1(data):
    total = 0
    for i, pair in enumerate(data.split("\n\n")):
        p1, p2 = map(eval, pair.split("\n"))
        total += (i + 1) * (compare(p1, p2) == -1)
    return total


def part2(data):
    values = [eval(p) for p in data.split("\n") if p]
    delimiters = [[[2]], [[6]]]
    values += delimiters
    values = sorted(values, key=functools.cmp_to_key(compare))
    return prod(i for i, val in enumerate(values, start=1)
                if val in delimiters)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
