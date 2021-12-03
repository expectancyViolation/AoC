from collections import Counter
from typing import List

from util import *

DAY = 3
YEAR = 2021


def get_best(counter: Counter):
    return 1 if counter[1] >= counter[0] else 0


def to_num(bin_digits: List[int]):
    return int("".join(map(str, bin_digits)), 2)


def get_consumption(rate1: List[int], rate2: List[int]):
    rate1 = to_num(rate1)
    rate2 = to_num(rate2)
    return rate1 * rate2


def part1(power: List[List[int]]):
    cols = [Counter(x) for x in zip(*power)]
    gamma = [get_best(x) for x in cols]
    epsilon = [1 - get_best(x) for x in cols]
    return get_consumption(gamma, epsilon)


def filter_common_digits(power: List[List[int]], low: bool):
    index = 0
    while len(power) > 1:
        best = get_best(Counter(x[index] for x in power))
        power = [x for x in power if (x[index] == best) ^ low]
        index += 1
    return data[0]


def part2(power: List[List[int]]):
    oxy = filter_common_digits(power, low=True)
    co2 = filter_common_digits(power, low=False)
    return get_consumption(oxy, co2)


if __name__ == "__main__":
    input_lines = get_data(DAY, year=YEAR, raw=True).split("\n")
    data = [[*map(int, x)] for x in input_lines]
    print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
