from util import *

DAY = 6
YEAR = 2022


def solve(data, run_len):
    for i in range(len(data)):
        if len({*data[i:i + run_len]}) == run_len:
            return i + run_len


def part1(data):
    return solve(data, 4)


def part2(data):
    return solve(data, 14)


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)[0]
    print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
