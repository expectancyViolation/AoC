from collections import defaultdict
from itertools import product

import numpy as np

from util import *

DAY = 20
YEAR = 2021


# weird step assumes inverse boundary condition (i.e. everything outside is on)
def step(lookup, image, weird=False):
    new_image = defaultdict(lambda: 0)
    boundary = set()
    for (i, j), _pixel in image.items():
        for di, dj in product(range(-1, 2), repeat=2):
            boundary.add((i + di, j + dj))

    for (i, j) in boundary:
        res = 0
        for di, dj in product(range(-1, 2), repeat=2):
            npos = (i + di, j + dj)
            res = 2 * res + (((npos in image) and (image[npos])) or (
                    weird and npos not in image))
        out = lookup[res]
        new_image[(i, j)] = out
    return new_image


def solve(steps, lookup, data):
    assert steps % 2 == 0
    image = defaultdict(lambda: 0,
                        {(i, j): x == "#" for i, line in
                         enumerate(data.split("\n")) for
                         j, x in
                         enumerate(line)})
    lookup = [x == "#" for x in lookup]
    for _ in range(steps // 2):
        image = step(lookup, image)
        image = step(lookup, image, weird=True)
    return sum(1 for v in image.values() if v)

@timing
def part1(lookup, data):
    return solve(2, lookup, data)

@timing
def part2(data):
    return solve(50, lookup, data)


if __name__ == "__main__":
    raw_data = get_data(DAY, year=YEAR, raw=True)
    lookup, data = raw_data.split("\n\n")
    res = part1(lookup, data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
