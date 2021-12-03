from collections import Counter

from util import *

DAY = 3
YEAR = 2021


def part1(data):
    cols = [Counter(x) for x in zip(*data)]
    gamma = ["1" if x["1"] > x["0"] else "0" for x in cols]
    epsilon = ["1" if x["1"] < x["0"] else "0" for x in cols]
    gamma = int("".join(gamma), 2)
    epsilon = int("".join(epsilon), 2)
    return gamma * epsilon


def filter(data, high):
    index = 0
    while len(data) > 1:
        C = Counter([x[index] for x in data])
        best = "1" if C["1"] >= C["0"] else "0"
        data = [x for x in data if (x[index] == best) ^ high]
        index += 1
    return data[0]


def part2(data):
    oxy = filter(data, high=True)
    co2 = filter(data, high=False)
    oxy = int("".join(oxy), 2)
    co2 = int("".join(co2), 2)
    return oxy * co2


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True).split("\n")
    print(data)
    # res = part1(data)
    # print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
