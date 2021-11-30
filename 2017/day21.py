import numpy as np

from util import *

DAY = 21
YEAR = 2017


def transform(data, lookup):
    L = len(data)
    n = 2 + (L % 2)
    m = n + 1
    mapped = np.array([[lookup(data[i:i + n, j:j + n]) for j in range(0, L, n)] for i in range(0, L, n)])
    mapped = np.stack(mapped, axis=1)
    mapped = np.stack(mapped, axis=2)
    return mapped.reshape(L // n * m, L // n * m)


INITIAL_DATA = """.#.
..#
###"""


def resquare(string):
    return [[*x] for x in string.split("/")]


def unsquare(square):
    return "/".join("".join(x) for x in square)


def solve(rules, n):
    def trafo(string, n_rot: int, flip: bool):
        resquared = resquare(string)
        for _ in range(n_rot):
            resquared = [*zip(*resquared[::-1])]
        if flip:
            resquared = [x[::-1] for x in resquared]
        return unsquare(resquared)

    rules = {trafo(x, i, flip): y for x, _, y in rules for i in range(4) for flip in (True, False)}

    def lookup(arr):
        return resquare(rules[unsquare(arr)])

    data = np.array([x.split("\n") for x in INITIAL_DATA.split("\n")])
    for i in range(n):
        data = transform(data, lookup)
        print(i)
        # print(data)
    return np.sum(data == "#")


def part1(rules):
    return solve(rules, 5)


def part2(rules):
    return solve(rules, 18)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    print(data)
    # res = part1(data)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    submit(DAY, 2, res, year=YEAR)
