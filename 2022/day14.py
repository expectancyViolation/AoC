import re

import numpy as np

from util import *

DAY = 14
YEAR = 2022


def part1(data):
    coords = [[[int(x) for x in point.split(",")]
               for point in re.findall(r"([0-9]+,[0-9]+)", row)] for row in
              data.split("\n")]
    mx = max(coord[0] for row in coords for coord in row)
    my = max(coord[1] for row in coords for coord in row)
    print(mx)
    sand = np.zeros([mx + 10, my + 10], dtype=int)
    for row in coords:
        lx, ly = row[0]
        for x, y in row[1:]:
            a, b = sorted([x, lx])
            c, d = sorted([y, ly])
            sand[a:b + 1, c:d + 1] = 1
            lx, ly = x, y

    print(sand[493:505, 0:10])
    while True:
        cx, cy = 500, 0
        while cy <= my + 2:
            print(cx, cy)
            for dx, dy in (0, 1), (-1, 1), (1, 1):
                nx, ny = cx + dx, cy + dy
                if sand[nx][ny] == 0:
                    cx, cy = nx, ny
                    break
            else:
                break
        if cy <= my:
            sand[cx][cy] = 2
        else:
            print("broken", cx, cy)
            break
    return np.sum(sand == 2)


def part2(data):
    coords = [[[int(x) for x in point.split(",")]
               for point in re.findall(r"([0-9]+,[0-9]+)", row)] for row in
              data.split("\n")]
    mx = max(coord[0] for row in coords for coord in row)
    my = max(coord[1] for row in coords for coord in row)
    print(mx)
    sand = np.zeros([mx + 500, my + 10], dtype=int)
    for row in coords:
        lx, ly = row[0]
        for x, y in row[1:]:
            a, b = sorted([x, lx])
            c, d = sorted([y, ly])
            sand[a:b + 1, c:d + 1] = 1
            lx, ly = x, y

    sand[:, my + 2] = 1

    while True:
        cx, cy = 500, 0
        while cy <= my + 4:
            for dx, dy in (0, 1), (-1, 1), (1, 1):
                nx, ny = cx + dx, cy + dy
                if sand[nx][ny] == 0:
                    cx, cy = nx, ny
                    break
            else:
                break
        if cy <= my+3 and cy > 0:
            sand[cx][cy] = 2
        else:
            print("broken", cx, cy)
            break
    return np.sum(sand == 2)+1


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True)
    # data = get_data(DAY, year=YEAR, raw=True, filename="input/2022/14_test.txt")
    print(data)
    # res = part1(data)
    # print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    submit(DAY, 2, res,year=YEAR)
