from util import *

DAY = 1
YEAR = 2022


def part1(data):
    groups = data.split("\n\n")
    group_values = [sum(int(x) for x in group.split()) for group in groups]
    return max(group_values)


def part2(data):
    groups = data.split("\n\n")
    group_values = [sum(int(x) for x in group.split()) for group in groups]
    group_values.sort()
    return sum(group_values[-3:])


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True)
    print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(data)
    print(res)
    submit(DAY, 2, res, year=YEAR)
