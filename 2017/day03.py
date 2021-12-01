from collections import defaultdict
from itertools import count, product

from util import *

DAY = 3
YEAR = 2017

rotations = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def part1(data):
    return 0


def part2(data):
    values = defaultdict(lambda: 0)
    rot_index = 2
    x, y = 0, 0
    n = 1

    def get_sum(x, y):
        if x == y == 0:
            return 1
        res = 0
        for dx, dy in product(range(-1, 2), repeat=2):
            if 0 == dx == dy:
                continue
            nx, ny = x + dx, y + dy
            res += values[(nx, ny)]
        return res

    for i in count():
        for _ in range(2):
            dx, dy = rotations[rot_index]
            rot_index = (rot_index + 1) % 4
            for _ in range(i + 1):
                val = get_sum(y, -x)
                values[(y, -x)] = val
                x, y = x + dx, y + dy
                n += 1
                if val > data[0]:
                    return val


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    print(data)
    # res = part1(data)
    res = part2(data)
    # for x in range(-5, 6):
    #     print(" ".join(f"{res[(x, y)]:03}" for y in range(-5, 6)))

    print(res)
    # submit(DAY, 1, res,year=YEAR)
    submit(DAY, 2, res, year=YEAR)
