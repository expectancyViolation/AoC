from util import *
from heapq import heappush, heappop

DAY = 20
YEAR = 2016


def parse_line(line):
    return [*map(int, line.split("-"))]


def part1(data):
    curr = 0
    for low, high in data:
        if low <= curr:
            curr = high + 1
    return curr


def part2(data, limit=2**32):
    data = sorted(data, key=lambda x: x[0])
    closing = 0
    res = 0
    for low, high in data:
        res += max(0, low - closing - 1)
        closing = max(high, closing)
    return res + limit - closing - 1


if __name__ == "__main__":
    data = [*map(parse_line, get_data(DAY, year=YEAR))]
    data.sort(key=lambda x: x[1])

    # res = part1(data)
    # test_data = [[5, 8], [0, 2], [4, 7]]
    # res = part2(test_data, limit=10)
    #
    res = part2(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    submit(DAY, 2, res, year=YEAR)
