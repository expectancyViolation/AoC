import re

import numpy as np
from PIL import ImageOps

from util import *

DAY = 14
YEAR = 2022


def simulate(cave_layout, max_depth):
    while True:
        cx, cy = 500, 0
        while cy <= max_depth + 2:
            for dx, dy in (0, 1), (-1, 1), (1, 1):
                nx, ny = cx + dx, cy + dy
                if cave_layout[nx][ny] == 0:
                    cx, cy = nx, ny
                    break
            else:  # no valid move left
                break
        if max_depth >= cy > 0:
            cave_layout[cx][cy] = 2
        else:
            print("broken", cx, cy)
            break


def generate_cave_layout(data):
    coords = [[[int(x) for x in point.split(",")]
               for point in re.findall(r"([0-9]+,[0-9]+)", row)]
              for row in data.split("\n")]
    max_x = max(coord[0] for row in coords for coord in row)
    max_depth = max(coord[1] for row in coords for coord in row)
    # part 2 might lead to x of size max_x+max_depth(b.c. of 45° angle)
    cave = np.zeros([max_x + max_depth + 10, max_depth + 10], dtype=np.uint8)
    for row in coords:
        lx, ly = row[0]
        for x, y in row[1:]:
            a, b = sorted([x, lx])
            c, d = sorted([y, ly])
            cave[a:b + 1, c:d + 1] = 1
            lx, ly = x, y
    return cave, max_depth


def part1(data):
    cave, max_depth = generate_cave_layout(data)
    simulate(cave, max_depth)
    return np.sum(cave == 2)


def part2(data):
    cave, max_depth = generate_cave_layout(data)
    cave[:, max_depth + 2] = 1
    simulate(cave, max_depth + 2)
    img = Image.fromarray(cave * 100, 'L')
    img = ImageOps.mirror(img.rotate(-90, expand=True))
    img.save("/tmp/lul_.png")
    return np.sum(cave == 2) + 1  # include uppermost point of "pyramid"


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR, raw=True)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res, year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
