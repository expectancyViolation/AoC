import networkx as nx
import numpy as np

from util import *
from day10 import knot_hash

from scipy.ndimage.measurements import label

DAY = 14
YEAR = 2017


def get_grid(data):
    total = []
    for i in range(128):
        start = f"{data}-{i}"
        res = "0x" + knot_hash(start)
        val = int(res, 16)
        total.append([1 * (x == "1") for x in (f"{val:0128b}")])
    return total


def part1(data):
    return np.sum(get_grid(data))


def part2(data):
    grid = get_grid(data)
    _, n_components = label(grid)
    return n_components


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)[0]
    print(data)
    # res = part1(data)
    res = part2(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    submit(DAY, 2, res,year=YEAR)
