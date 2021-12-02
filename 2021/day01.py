import numpy as np
from matplotlib import pyplot as plt

from util import *

DAY = 1
YEAR = 2021


def part1(data):
    return sum(x < y for x, y in zip(data, data[1:]))


def part2(data):
    return sum(x < y for x, y in zip(data, data[3:]))


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    print(data)
    plt.plot(data)
    plt.show()
    # res = part1(data)
    # print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
