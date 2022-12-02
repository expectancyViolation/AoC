from util import *

DAY = 1
YEAR = 2022


def get_group_values(data):
    groups = data.split("\n\n")
    return [sum(int(x) for x in group.split()) for group in groups]


def part1(data):
    group_values = get_group_values(data)
    return max(group_values)


def part2(data):
    group_values = get_group_values(data)
    group_values.sort()
    return sum(group_values[-3:])


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
