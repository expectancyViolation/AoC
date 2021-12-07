import numpy as np

from util import *

DAY = 7
YEAR = 2021


def part1(data):
    optimal = np.round(np.median(data))
    return int(np.sum(np.abs(data - optimal)))


def part2(data):
    optimal = int(np.mean(data))
    res = inf
    # around that point
    for x in range(optimal - 2, optimal + 2):
        distances = np.abs(data - x)
        res = min(res, int(np.sum(distances * (distances + 1) / 2)))
    return res


if __name__ == "__main__":
    raw_data = get_data(DAY, year=YEAR, raw=True)
    data = [*map(int, raw_data.split(","))]
    data = np.array(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)

