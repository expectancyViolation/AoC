from math import prod

import numpy as np
from scipy.ndimage.measurements import label

from util import *

DAY = 9
YEAR = 2021


@timing
def solve(arr):
    p = np.pad(arr, 1, constant_values=9)
    low_points = (p < np.minimum.reduce([
        np.roll(p, 1, axis=0),
        np.roll(p, -1, axis=0),
        np.roll(p, 1, axis=1),
        np.roll(p, -1, axis=1)
    ]))
    risk_level = np.sum(p[low_points] + 1)
    labeled, n = label(arr != 9)
    unique, counts = np.unique(labeled, return_counts=True)
    size_prod = prod(sorted(counts)[-4:-1])
    return risk_level, size_prod


if __name__ == "__main__":
    raw_data = get_data(DAY, year=YEAR, raw=True)
    arr = np.array([[int(x) for x in line] for line in raw_data.split("\n")],
                   dtype=int)
    part1, part2 = solve(arr)
    print(part1)
    # submit(DAY, 1, part1,year=YEAR)
    print(part2)
    # submit(DAY, 2, part2, year=YEAR)
