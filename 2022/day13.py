import functools

from util import *

DAY = 13
YEAR = 2022


def compare(l1, l2):
    if isinstance(l1, int):
        l1 = [l1]
    if isinstance(l2, int):
        l2 = [l2]
    if len(l1) == 0 and len(l2) == 0:
        return 0
    if len(l1) == 0:
        return -1

    if len(l2) == 0:
        return 1

    left = l1[0]
    right = l2[0]
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        if left > right:
            return 1
        return compare(l1[1:], l2[1:])
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    for x, y in zip(left, right):
        c = compare(x, y)
        if c:
            return c
    l_left = len(left)
    l_right = len(right)
    if l_left < l_right:
        return -1
    if l_right < l_left:
        return 1
    return compare(l1[1:], l2[1:])


def part1(data):
    total = 0
    for i, pair in enumerate(data.split("\n\n")):
        p1, p2 = pair.split("\n")
        p1 = eval(p1)
        p2 = eval(p2)
        res = compare(p1, p2)
        assert res != 0
        if res == -1:
            total += (i + 1)
    return total


def part2(data):
    values = [eval(p) for pair in data.split("\n\n") for p in pair.split("\n")]
    delimiters = [[[2]], [[6]]]
    values += delimiters
    values = sorted(values, key=functools.cmp_to_key(compare))
    res = 1
    for i, val in enumerate(values, start=1):
        print(val, val in delimiters)
        if val in delimiters:
            res *= i
    return res


if __name__ == "__main__":
    # data = get_data(DAY, year=YEAR, raw=True, filename="input/2022/13_test.txt")
    data = get_data(DAY, year=YEAR, raw=True)
    # print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    submit(DAY, 2, res,year=YEAR)
