from util import *

DAY = 4
YEAR = 2022


def parse_pair(pair):
    return [int(x) for x in pair.split("-")]


def parse_row(row):
    pairs = row.split(",")
    return [parse_pair(pair) for pair in pairs]


def part1(data):
    res = 0
    for row in data:
        (p1_low, p1_high), (p2_low, p2_high) = parse_row(row)
        fully_contain = (p1_low - p2_low) * (p1_high - p2_high) <= 0
        res += fully_contain
    return res


def part2(data):
    res = 0
    for row in data:
        (p1_low, p1_high), (p2_low, p2_high) = parse_row(row)
        no_overlap = (p1_high < p2_low) | (p2_high < p1_low)
        res += not no_overlap
    return res


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res,year=YEAR)
