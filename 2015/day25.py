import re

from util import *

DAY = 25
YEAR = 2015


@timing
def part1(data):
    row, column = map(int, re.findall(r"[0-9]+", data))
    diagonals_cnt = row + column - 2
    diagonals_skipped = diagonals_cnt * (diagonals_cnt + 1) // 2
    diagonal_skipped = column - 1
    skipped = diagonals_skipped + diagonal_skipped
    return (20151125 * pow(252533, skipped, 33554393)) % 33554393


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True)
    print(data)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
