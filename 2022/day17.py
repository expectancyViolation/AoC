from collections import defaultdict
from itertools import cycle

import numpy as np

from util import *

DAY = 17
YEAR = 2022


def gen_rocks():
    with open("17_rocks.txt", "r") as f:
        rocks = [rock.split("\n") for rock in f.read().split("\n\n")]
    yield from cycle(rocks)


def gen_jets(data):
    for x in cycle(data):
        yield "< >".index(x) - 1


def render_filling(filled, y_min=0):
    y_max = max(y for x, y in filled)
    cave = np.zeros([y_max + 1 - y_min, 7], dtype=int)
    for x, y in filled:
        y -= y_min
        if y >= 0:
            cave[-1 - y, x] = 1
    print("-----")
    for line in cave:
        print("".join(map(lambda x: ".#@"[x], line)))


def simulate(data, n_steps=2022, hash_depth=50):
    rocks_gen = gen_rocks()
    jet_period = len(data)
    piece_period = 5
    jet_gen = gen_jets(data)
    jet_count = 0
    filled = set()
    curr_height = 0
    hashes = defaultdict(lambda: dict())

    def gen_rock_positions(rock, x, y):
        for i, line in enumerate(rock[::-1]):
            for j, val in enumerate(line):
                if val == "#":
                    yield x + j, i + y

    def check_valid_position(rock, x, y):
        return all(all(((0 <= rx < 7), ry >= 0, (rx, ry) not in filled))
                   for rx, ry in gen_rock_positions(rock, x, y))

    def hash_top_layers():
        to_hash = []
        for x, y in filled:
            y = y - curr_height + hash_depth
            if y >= 0:
                to_hash.append((x, y))
        return hash(tuple(sorted(to_hash)))

    periodic_height = 0
    period_found = False
    rock_count = 0

    def check_period_by_hash():
        if curr_height < hash_depth:
            return
        new_hash = hash_top_layers()
        rock_index = rock_count % piece_period
        curr_hashes = hashes[(jet_count, rock_index)]
        if new_hash in curr_hashes:
            old_i, old_height = curr_hashes[new_hash]
            period = rock_count - old_i
            height_step = curr_height - old_height
            return period, height_step
        curr_hashes[new_hash] = (rock_count, curr_height)

    def try_advance_period():
        nonlocal rock_count, periodic_height, period_found
        hash_response = check_period_by_hash()
        if hash_response is not None:
            period, height_step = hash_response
            # print("found period",period,height_step)
            period_found = True
            remaining_steps = n_steps - rock_count - 1
            periodic_steps = (remaining_steps // period) * period
            periodic_height = (remaining_steps // period) * height_step
            rock_count += periodic_steps

    while rock_count < n_steps:
        rock = next(rocks_gen)
        if not period_found:
            try_advance_period()

        rx, ry = 2, curr_height + 3
        while True:
            # move jet
            jet = next(jet_gen)
            jet_count = (jet_count + 1) % jet_period
            nx, ny = rx + jet, ry
            if check_valid_position(rock, nx, ny):
                rx, ry = nx, ny
            # fall
            nx, ny = rx, ry - 1
            if check_valid_position(rock, nx, ny):
                rx, ry = nx, ny
            else:
                # freeze rock
                filled |= {*gen_rock_positions(rock, rx, ry)}
                curr_height = max(
                    curr_height,
                    1 + max(y for x, y in gen_rock_positions(rock, rx, ry)))
                break
        rock_count += 1
    return filled, periodic_height


@timing
def part1(data):
    filled, periodic_height = simulate(data, 2022)
    height = max(y for x, y in filled) + 1 + periodic_height
    # render_filling(filled, height - 10)
    return height


@timing
def part2(data):
    filled, periodic_height = simulate(data, 1_000_000_000_000)
    height = max(y for x, y in filled) + 1 + periodic_height
    return height


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR,filename="input/2022/17_test.txt", raw=True)
    res = part1(data)
    print(res)
    # submit(DAY, 1, res,year=YEAR)
    res = part2(data)
    print(res)
    # submit(DAY, 2, res, year=YEAR)
