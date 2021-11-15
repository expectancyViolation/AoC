import re

import numpy as np

from util import *

DAY = 8


def apply_row(screen, row):
    if m := re.match(r"rect ([0-9]+)x([0-9]+)", row):
        x, y = map(int, m.groups())
        screen[:y, :x] = 1
    elif m := re.match(r"rotate column x=([0-9]+) by ([0-9]+)", row):
        x, rot = map(int, m.groups())
        rot = (-rot) % len(screen)
        screen[:, x] = np.concatenate((screen[rot:, x], screen[:rot, x]))
    elif m := re.match(r"rotate row y=([0-9]+) by ([0-9]+)", row):
        y, rot = map(int, m.groups())
        rot = (-rot) % len(screen[0])
        screen[y, :] = np.concatenate((screen[y, rot:], screen[y, :rot]))


def part1(data):
    screen = np.zeros([6, 50],dtype=np.uint8)
    for row in data:
        apply_row(screen, row)
        print(row)
        for row in screen:
            print("".join(map(lambda x: "X" if x else " ",row)))
    return np.sum(screen)


def part2(data):
    return 0


if __name__ == "__main__":
    data = get_data(DAY, raw=True).split("\n")
    res = part1(data)
    # res = part2(data)
    print(res)
    # submit(DAY, 1, res)
    # part2 manually inserted
    # submit(DAY, 2, res)
