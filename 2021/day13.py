import re

import numpy as np

from util import *

DAY = 13
YEAR = 2021


def solve(coords, folds):
    bounds = [max(coord[i] for coord in coords) + 1 for i in range(2)]
    paper = np.zeros([x + (x % 2 == 0) for x in bounds[::-1]], dtype=bool)
    for x, y in coords:
        paper[y, x] = 1
    for fold_dir, fold_pos in folds:
        if fold_dir == "x":
            paper = (paper[:, :fold_pos] + paper[:, :fold_pos:-1]) > 0
        if fold_dir == "y":
            paper = (paper[:fold_pos, :] + paper[:fold_pos:-1, :]) > 0
    return paper


def part1(coords, folds):
    paper = solve(coords, folds[:1])
    return np.sum(paper)


def part2(coords, folds):
    paper = solve(coords, folds).astype(int)
    for line in paper:
        print("".join("X" if x else " " for x in line))


def parse_fold(line):
    m = re.match(r"fold along (\w)=(\d+)", line)
    direction, pos = m.groups()
    return direction, int(pos)


if __name__ == "__main__":
    coords, folds = get_data(DAY, year=YEAR, raw=True).split("\n\n")
    coords = [[*map(int, line.split(","))] for line in coords.split("\n")]
    folds = [parse_fold(line) for line in folds.split("\n")]
    res = part1(coords, folds)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    part2(coords, folds)
    # TODO: OCR? :D
    # submit(DAY, 2, res,year=YEAR)
