import re

from util import *

DAY = 25
YEAR = 2015


def part1(data):
    row, column = map(int, re.findall(r"[0-9]+", data))
    diagonals_cnt = row + column - 2
    diagonals_skipped = diagonals_cnt * (diagonals_cnt + 1) // 2
    diagonal_skipped = column - 1
    skipped = diagonals_skipped + diagonal_skipped
    res = 20151125
    for _ in range(skipped):
        res = (res * 252533) % 33554393
    return res


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True)
    print(data)
    res = part1(data)
    print(res)
    submit(DAY, 1, res, year=YEAR)
    # res = part2(data)
    # print(res)
    # submit(DAY, 2, res,year=YEAR)
