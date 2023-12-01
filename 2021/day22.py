import re

import numpy as np

from util import *

DAY = 22
YEAR = 2021


def parse_row(row):
    on = "on" in row
    coords = re.findall(r"(-?\d+)..(-?\d+)", row)
    return on, [[int(x), int(y) + 1] for x, y in coords]


def solve(data):
    splitters = [sorted(set(x for _on, cube in data for x in cube[i])) for i in
                 range(3)]
    sizes = [(np.diff(arr)).astype(np.longlong) for arr in splitters]
    vols = np.einsum('i,j,k->ijk', *sizes)

    splitter_data = [
        (on, [[splitters[i].index(x) for x in cube[i]] for i in range(3)]) for
        on, cube in data]

    grid = np.zeros([len(x) - 1 for x in splitters], dtype=bool)

    for on, cube in splitter_data:
        grid[tuple(slice(*x) for x in cube)] = on
    return np.sum(vols[grid])


@timing
def part1(data):
    # DANGER: used 51 since my ranges are right exclusive (see parse)
    p1_data = [(on, cube) for on, cube in data if all(
        all(abs(x) <= 51 for x in d) for d in cube)]
    return solve(p1_data)


@timing
def part2(data):
    return solve(data)


if __name__ == "__main__":
    raw_data = get_data(DAY, year=YEAR, raw=True)
    data = [*map(parse_row, raw_data.split("\n"))]
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
