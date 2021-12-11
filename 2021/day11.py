from itertools import count

import numpy as np
from scipy import signal

from util import *

DAY = 11
YEAR = 2021

NBs = np.ones([3, 3], dtype=np.uint8)
NBs[1, 1] = 0


def step(arr):
    arr += 1
    total_flashed = np.zeros(arr.shape, dtype=np.uint8)
    while True:
        flashed = arr > 9
        if not np.any(flashed):
            break
        arr[flashed] = 0
        increases = signal.convolve2d(flashed, NBs, mode="same")
        arr += increases
        total_flashed |= flashed
    arr[total_flashed != 0] = 0


def part1(arr):
    res = 0
    for i in range(100):
        step(arr)
        res += np.sum(arr == 0)
    return res


def part2(arr):
    for i in count(1):
        step(arr)
        if np.sum(arr == 0) == arr.size:
            return i


if __name__ == "__main__":
    raw_data = get_data(DAY, year=YEAR, raw=True)
    arr = np.array([[*map(int, line)] for line in raw_data.split("\n")],
                   dtype=np.uint8)
    res = part1(arr)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(arr)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
