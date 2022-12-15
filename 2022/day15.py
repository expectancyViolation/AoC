import re
from collections import defaultdict
from itertools import product

from util import *

DAY = 15
YEAR = 2022


def part1(data):
    Y = 2000000
    no_beacon = set()
    beacon = set()
    for row in data:
        # print(len(no_beacon))
        res = map(int, re.findall("(\-?[0-9]+)", row))
        sx, sy, bx, by = res
        beacon.add((bx, by))
        # print(row, sx, sy, bx, by)
        d = abs(bx - sx) + abs(by - sy)
        for x in range(sx - d - 5, sx + d + 5):
            d_curr = abs(sx - x) + abs(sy - Y)
            if d_curr <= d:
                no_beacon.add((x, Y))
    return sum(1 for x, y in no_beacon - beacon if y == Y)


def manhattan(x, y, a, b):
    return abs(x - a) + abs(y - b)


def part2(data):
    border_cnt = defaultdict(lambda: 0)
    stations = []
    for row in data:
        print(len(border_cnt))
        # print(len(no_beacon))
        res = map(int, re.findall("(\-?[0-9]+)", row))
        sx, sy, bx, by = res
        d = manhattan(bx, by, sx, sy)
        stations += [(sx, sy, d)]
        cx, cy = sx + d + 1, sy
        border = set()
        for dx, dy in (-1, 1), (-1, -1), (1, -1), (1, 1):
            while True:
                nx, ny = cx + dx, cy + dy
                if manhattan(nx, ny, sx, sy) != d + 1:
                    break
                else:
                    cx, cy = nx, ny
                    border.add((cx, cy))
        for p in border:
            border_cnt[p] += 1
    candidates = [x for x, cnt in border_cnt.items() if cnt >= 4]
    for cx, cy in candidates:
        if all(manhattan(cx, cy, sx, sy) > d for sx, sy, d in stations):
            return cx * 4000000 + cy


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True).split("\n")
    print(len(data))
    # data = get_data(DAY, year=YEAR, raw=True,
    #                 filename="input/2022/15_test.txt").split("\n")
    # print(data)
    # res = part1(data)
    # print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    submit(DAY, 2, res, year=YEAR)
