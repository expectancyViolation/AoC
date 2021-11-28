from itertools import count

from util import *

DAY = 13
YEAR = 2017


def score(data, offset=0):
    res = 0
    passed = True
    for depth, range in data:
        n = 2 * (range - 1)
        if (depth + offset) % n == 0:
            res += depth * range
            passed = False
    return res, passed


def part1(data):
    res, _ = score(data)
    return res


def part2(data):
    for i in count():
        if i % 10000 == 0:
            print(i)
        _, passed = score(data, i)
        if passed:
            return i


if __name__ == "__main__":
    data = [[*map(int, line.split(":"))]
            for line in get_data(DAY, year=YEAR, raw=True).split("\n")]
    print(data)
    # res = part1(data)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    submit(DAY, 2, res, year=YEAR)
