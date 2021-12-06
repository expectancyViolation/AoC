from collections import Counter, defaultdict
from functools import lru_cache

import numpy as np

from helpers import mat_pow_mod, mat_dot
from util import *

DAY = 6
YEAR = 2021


@lru_cache()
def get_transition_matrix():
    M = [[0] * 9 for _ in range(9)]
    for i in range(8):
        M[i][i + 1] = 1
    M[6][0] = 1
    M[8][0] = 1
    return M


def solve(data, n):
    M = get_transition_matrix()
    res = mat_pow_mod(M, n, 10 ** 100)
    return sum(mat_dot(res, data))

@timing
def part1(data):
    return solve(data, 80)

@timing
def part2(data):
    return solve(data, 256)


def get_counts(data_raw):
    data = Counter([*map(int, data_raw.split(","))])
    counts = [0] * 9
    for n, i in data.items():
        counts[n] = i
    return counts


if __name__ == "__main__":
    data_raw = get_data(DAY, year=YEAR, raw=True)
    # data_raw = "3,4,3,1,2"
    counts = get_counts(data_raw)
    res = part1(counts)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(counts)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
