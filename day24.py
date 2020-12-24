import re
import numpy as np
from collections import Counter, defaultdict
from util import *

DAY = 24

A = np.array

DIRECTIONS = {
    "e": A((1, 0)),
    "nw": A((0, 1)),
    "ne": A((1, 1)),
    "w": A((-1, 0)),
    "sw": A((-1, -1)),
    "se": A((0, -1))
}


def part1(data):
    pattern = re.compile("|".join(DIRECTIONS))
    end_positions = [
        tuple(sum(DIRECTIONS[step] for step in pattern.findall(tile)))
        for tile in data
    ]
    tile_counts = Counter(end_positions)
    black_tiles = [x for x, c in tile_counts.items() if c % 2 == 1]
    return black_tiles


def step(locations):
    neighbors = defaultdict(lambda: 0)
    # sample random location for the dimension:
    for d_vec in DIRECTIONS.values():
        if not any(d_vec):
            continue
        for vec in locations:
            neighbors[tuple(x + dx for x, dx in zip(vec, d_vec))] += 1
    new_locations = set()
    for loc in locations:
        if 1 <= neighbors[loc] <= 2:
            new_locations.add(loc)
    for loc, nbs in neighbors.items():
        if nbs == 2 and loc not in locations:
            new_locations.add(loc)
    return new_locations


def part2(black_tiles):
    for i in range(100):
        black_tiles = step(black_tiles)
        #print(len(black_tiles))
    return len(black_tiles)


if __name__ == "__main__":
    data = get_data(DAY)
    #print(data)

    black_tiles = part1(data)
    res = len(black_tiles)
    #submit(DAY, 1, res)

    res = part2(black_tiles)
    print(res)
    submit(DAY, 2, res)
